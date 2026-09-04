#!/usr/bin/env python3
"""Serveur statique multi-thread pour le site C-LINE (évite les pages tronquées
du http.server mono-thread quand la page charge beaucoup de ressources)."""
import functools
import http.server
import socketserver

PORT = 8741
ROOT = "/Users/dreyfus/C-LINE/site"


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):
        pass


class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    handler = functools.partial(Handler, directory=ROOT)
    with ThreadingServer(("", PORT), handler) as httpd:
        print(f"Serving {ROOT} on http://localhost:{PORT} (threading)")
        httpd.serve_forever()
