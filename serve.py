"""Static server for the trip board.

Plain `python -m http.server` sends Last-Modified with no Cache-Control, which
lets browsers heuristically cache index.html -- you edit the page, reload, and
still get the old JavaScript. Everything here is served no-store.
"""
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    handler = partial(NoCacheHandler, directory=str(__import__("pathlib").Path(__file__).parent))
    print(f"trip board on http://localhost:{port} (no-store)")
    ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
