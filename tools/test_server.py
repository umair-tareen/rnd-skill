"""End-to-end test of server.py over real stdio JSON-RPC.

Launches the server exactly as an MCP client would (a subprocess speaking
newline-delimited JSON-RPC), performs the initialize handshake, lists tools,
then exercises a full thesis round-trip -- including the enforcement paths:
the derived demand stamp, the V10 typed-buyer-evidence refusal, and the
absolute-path guard. Run by CI on every push; `python tools/test_server.py`.

Requires: pip install mcp
"""
import json
import os
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

SERVER = str(Path(__file__).resolve().parent / "server.py")


class Client:
    def __init__(self):
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        self.p = subprocess.Popen([sys.executable, SERVER], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True, encoding="utf-8", env=env)
        self._id = 0
        # drain stderr so the server can never block on a full pipe
        threading.Thread(target=self.p.stderr.read, daemon=True).start()

    def send(self, obj):
        self.p.stdin.write(json.dumps(obj) + "\n")
        self.p.stdin.flush()

    def call(self, method, params=None):
        self._id += 1
        self.send({"jsonrpc": "2.0", "id": self._id, "method": method,
                   "params": params or {}})
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise SystemExit(f"server died during {method}")
            msg = json.loads(line)
            if msg.get("id") == self._id:
                if "error" in msg:
                    raise SystemExit(f"{method} -> error: {msg['error']}")
                return msg["result"]

    def notify(self, method, params=None):
        self.send({"jsonrpc": "2.0", "method": method, "params": params or {}})

    def tool(self, name, args, expect_error=False):
        res = self.call("tools/call", {"name": name, "arguments": args})
        if expect_error:
            assert res.get("isError"), f"{name} should have errored: {res}"
        else:
            assert not res.get("isError"), f"{name} isError: {res}"
        return "\n".join(c.get("text", "") for c in res.get("content", []))

    def close(self):
        try:
            self.p.stdin.close()
            self.p.wait(timeout=10)
        except Exception:
            self.p.kill()


def main():
    c = Client()
    try:
        init = c.call("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "handshake-test", "version": "0"},
        })
        assert init["serverInfo"]["name"] == "rnd", init["serverInfo"]
        c.notify("notifications/initialized")

        names = sorted(t["name"] for t in c.call("tools/list")["tools"])
        expected = {"thesis_new", "thesis_show", "thesis_stale", "claim_add",
                    "claim_set", "open_set", "flip_set", "verdict_set",
                    "diff_append", "thesis_compact", "squeeze_text",
                    "run_measure", "run_state"}
        assert expected <= set(names), expected - set(names)
        print(f"handshake + tools/list ok ({len(names)} tools)")

        with tempfile.TemporaryDirectory() as tmp:
            thesis = str(Path(tmp) / "acme.md")
            run = str(Path(tmp) / "acme-run-1")

            # absolute-path guard: a relative path is a protocol error, loudly
            c.tool("thesis_new", {"slug": "x", "title": "X",
                                   "path": "relative/nope.md"}, expect_error=True)
            print("relative path rejected ok")

            print(c.tool("thesis_new", {"slug": "acme", "title": "Acme",
                                         "path": thesis}))
            assert "REFUSED" in c.tool("thesis_new", {"slug": "acme",
                                                       "title": "Acme",
                                                       "path": thesis})
            c.tool("claim_add", {"path": thesis,
                                  "claim": "rivals bundle it free", "st": "V",
                                  "conf": 0.8, "source": "example.com",
                                  "falsifier": "a paying user cites none",
                                  "load_bearing": True, "cls": "world"})
            c.tool("claim_add", {"path": thesis, "claim": "teams will pay us",
                                  "st": "A", "conf": 0.3, "cls": "customer"})

            doc = json.loads(c.tool("thesis_show", {"path": thesis}))
            assert len(doc["claims"]) == 2
            assert doc["demand"]["unvalidated"] is True, doc["demand"]
            print(f"demand stamp fires over MCP: {doc['demand']['flag']}")

            # V10 over the protocol: free text cannot verify a customer claim
            out = c.tool("claim_set", {"path": thesis, "cid": "C2", "st": "V",
                                        "source": "pricing comparable"})
            assert out.startswith("REFUSED"), out
            print("V10 refusal over MCP ok")
            # typed buyer evidence clears it
            assert "revised" in c.tool("claim_set", {
                "path": thesis, "cid": "C2", "st": "V",
                "source": "buyer:call 2 teams booked a pilot"})
            doc = json.loads(c.tool("thesis_show", {"path": thesis}))
            assert doc["demand"]["unvalidated"] is False, doc["demand"]
            print("typed buyer evidence clears the stamp ok")

            # crash-safe run manifest
            c.tool("run_state", {"action": "init", "run_folder": run,
                                  "target": "Acme", "thesis": thesis})
            assert c.tool("run_state", {"action": "next",
                                         "run_folder": run}) == "FRAME"
            c.tool("run_state", {"action": "start", "run_folder": run,
                                  "move": "FRAME"})
            c.tool("run_state", {"action": "done", "run_folder": run,
                                  "move": "FRAME", "artifact": "00-frame.md"})
            assert c.tool("run_state", {
                "action": "next", "run_folder": run}) == "EVIDENCE-research"

            sq = json.loads(c.tool("squeeze_text",
                                    {"text": "\n".join(f"line {i}"
                                                        for i in range(40))}))
            assert sq["comp_lines"] < sq["orig_lines"]

        print("MCP SERVER TEST: PASS")
        return 0
    finally:
        c.close()


if __name__ == "__main__":
    sys.exit(main())
