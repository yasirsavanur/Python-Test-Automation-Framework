"""Serve the bundled UI and API on an ephemeral local port."""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


class DemoRequestHandler(SimpleHTTPRequestHandler):
    """Static file handler with two JSON API contracts."""

    def log_message(self, _format: str, *_args: object) -> None:
        return

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/health":
            self._send_json({"status": "ok", "service": "orbit-qa-store"})
            return
        if path == "/api/products":
            products_path = Path(self.directory, "products.json")
            products = json.loads(products_path.read_text(encoding="utf-8"))
            self._send_json({"count": len(products), "products": products})
            return
        super().do_GET()

    def _send_json(self, payload: object) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


@dataclass(slots=True)
class RunningDemoServer:
    server: ThreadingHTTPServer
    thread: threading.Thread

    @property
    def url(self) -> str:
        host, port = self.server.server_address
        return f"http://{host}:{port}"

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)


def start_demo_server(root: Path) -> RunningDemoServer:
    """Start a background server and return its lifecycle handle."""

    handler = partial(DemoRequestHandler, directory=str(root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, name="orbit-demo-server", daemon=True)
    thread.start()
    return RunningDemoServer(server=server, thread=thread)
