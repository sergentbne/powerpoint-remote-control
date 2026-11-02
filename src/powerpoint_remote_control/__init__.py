import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

import pyautogui
import qrcode

HOST = "0.0.0.0"
PORT = 8000

PAGE = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PowerPoint Remote</title>
<style>
  html, body { height: 100%; margin: 0; }
  body { display: grid; place-items: center; background: #111; }
  button {
    font-size: 8rem;
    padding: 2rem 4rem;
    border: none;
    border-radius: 2rem;
    background: #2d7d46;
    color: white;
    cursor: pointer;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
  }
  button:active { background: #1e5a32; transform: scale(.98); }
</style>
<button id="b" type="button">Next</button>
<script>
  document.getElementById('b').addEventListener('click', function () {
    fetch('/press', { method: 'POST' });
  });
</script>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        body = PAGE.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/press":
            self.send_error(404)
            return
        pyautogui.press("space")
        body = json.dumps({"ok": True}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {self.address_string()} {fmt % args}")


def local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


def main() -> None:
    server = HTTPServer((HOST, PORT), Handler)
    url = f"http://{local_ip()}:{PORT}"
    print(f"PPT remote: {url} — button press sends SPACE\n")
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii()
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
