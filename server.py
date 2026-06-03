#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"TOEIC 학습 서버 시작: http://localhost:{PORT}")
    print(f"아이패드에서 접속: http://<이 컴퓨터의 IP>:{PORT}")
    print("종료하려면 Ctrl+C를 누르세요.")
    httpd.serve_forever()
