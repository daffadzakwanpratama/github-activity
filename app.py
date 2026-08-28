import http.server
import socketserver
import json
import os
import sys
import subprocess
import webbrowser
import threading
import urllib.parse
import datetime
from typing import Tuple

PORT = 5000
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def _set_json_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_json_headers(200)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        
        if parsed_url.path == "/api/config":
            try:
                if os.path.exists(CONFIG_FILE):
                    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                else:
                    data = {}
                self._set_json_headers(200)
                self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))
            except Exception as e:
                self._set_json_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        # Serve static web files
        return super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        
        try:
            body = json.loads(post_body) if post_body else {}
        except Exception:
            body = {}

        # 1. Update Config
        if parsed_url.path == "/api/config":
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump(body, f, indent=2)
                self._set_json_headers(200)
                self.wfile.write(json.dumps({"success": True, "message": "Konfigurasi berhasil disimpan!"}).encode("utf-8"))
            except Exception as e:
                self._set_json_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        # 2. Run Daily Test
        if parsed_url.path == "/api/run-daily":
            force = body.get("force", False)
            try:
                cmd = [sys.executable, "daily.py"]
                if force:
                    # Jalankan langsung fungsi python dengan parameter force
                    proc = subprocess.run(
                        [sys.executable, "-c", "import daily; daily.make_daily_commits(force=True)"],
                        capture_output=True,
                        text=True
                    )
                else:
                    proc = subprocess.run(cmd, capture_output=True, text=True)
                
                output = proc.stdout + proc.stderr
                self._set_json_headers(200)
                self.wfile.write(json.dumps({"output": output.strip()}).encode("utf-8"))
            except Exception as e:
                self._set_json_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        # 3. Run Backfill
        if parsed_url.path == "/api/run-backfill":
            start_date_str = body.get("start_date")
            end_date_str = body.get("end_date")
            if not start_date_str or not end_date_str:
                self._set_json_headers(400)
                self.wfile.write(json.dumps({"error": "start_date dan end_date wajib diisi"}).encode("utf-8"))
                return
            
            try:
                code_snippet = f"""
import datetime, backfill
s = datetime.datetime.strptime('{start_date_str}', '%Y-%m-%d').date()
e = datetime.datetime.strptime('{end_date_str}', '%Y-%m-%d').date()
backfill.run_backfill(s, e)
"""
                proc = subprocess.run([sys.executable, "-c", code_snippet], capture_output=True, text=True)
                output = proc.stdout + proc.stderr
                self._set_json_headers(200)
                self.wfile.write(json.dumps({"output": output.strip()}).encode("utf-8"))
            except Exception as e:
                self._set_json_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        # 4. Git Push
        if parsed_url.path == "/api/git-push":
            try:
                proc = subprocess.run(
                    ["git", "push", "origin", "main"],
                    capture_output=True,
                    text=True
                )
                if proc.returncode != 0:
                    proc = subprocess.run(
                        ["git", "push", "origin", "master"],
                        capture_output=True,
                        text=True
                    )
                output = proc.stdout + proc.stderr
                self._set_json_headers(200)
                self.wfile.write(json.dumps({
                    "success": proc.returncode == 0,
                    "output": output.strip() or "Git push selesai dengan sukses."
                }).encode("utf-8"))
            except Exception as e:
                self._set_json_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self._set_json_headers(404)
        self.wfile.write(json.dumps({"error": "Endpoint tidak ditemukan"}).encode("utf-8"))

def open_browser():
    webbrowser.open(f"http://localhost:{PORT}")

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"==================================================")
        print(f"   🌱 GITHUB ACTIVITY DASHBOARD AKTIF              ")
        print(f"   🌐 Buka di browser: http://localhost:{PORT}     ")
        print(f"   Tekan Ctrl + C untuk mematikan server.         ")
        print(f"==================================================")
        
        # Buka browser otomatis setelah 1 detik
        threading.Timer(1.0, open_browser).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Server dimatikan.")
            httpd.server_close()

if __name__ == "__main__":
    run_server()
