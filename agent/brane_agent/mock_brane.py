"""Local stand-in for the BRANE gateway, for offline tests only.

It records every request body it receives so tests can assert exactly what
would have reached the external model. It does NOT reproduce real BRANE
detection behaviour; it only answers like an OpenAI-compatible endpoint.
"""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class MockBrane:
    def __init__(self, status: int = 200):
        self.received: list[dict] = []
        self.status = status
        mock = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
                mock.received.append(json.loads(body))
                if mock.status != 200:
                    self.send_response(mock.status)
                    self.end_headers()
                    return
                reply = {"choices": [{"message": {"role": "assistant", "content":
                         "PERSON_01: criterion 1 MET (mock answer). Requires human review."}}]}
                out = json.dumps(reply).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(out)))
                self.end_headers()
                self.wfile.write(out)

            def log_message(self, *args):
                pass

        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_port}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()

    def sent_text(self) -> str:
        return json.dumps(self.received, ensure_ascii=False)
