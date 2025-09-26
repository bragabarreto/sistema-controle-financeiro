#!/usr/bin/env python3
"""
Servidor simples que serve o frontend e redireciona APIs para o FastAPI
"""

import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
from urllib.parse import urlparse
import requests
import threading
import uvicorn
from app.main import app

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/home/ubuntu/financial-control-system/backend/app/static", **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # Se for uma requisição para a API, redirecionar para o FastAPI
        if parsed_path.path.startswith('/api/') or parsed_path.path in ['/docs', '/redoc', '/openapi.json']:
            try:
                response = requests.get(f'http://localhost:8001{self.path}')
                self.send_response(response.status_code)
                for header, value in response.headers.items():
                    if header.lower() not in ['content-encoding', 'transfer-encoding', 'connection']:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.content)
                return
            except:
                self.send_error(502, "Backend API not available")
                return
        
        # Para outras requisições, servir arquivos estáticos
        if parsed_path.path == '/' or parsed_path.path == '':
            self.path = '/index.html'
        
        return super().do_GET()
    
    def do_POST(self):
        # Redirecionar POSTs para a API
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith('/api/'):
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                
                response = requests.post(
                    f'http://localhost:8001{self.path}',
                    data=post_data,
                    headers=dict(self.headers)
                )
                
                self.send_response(response.status_code)
                for header, value in response.headers.items():
                    if header.lower() not in ['content-encoding', 'transfer-encoding', 'connection']:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.content)
                return
            except:
                self.send_error(502, "Backend API not available")
                return
        
        self.send_error(404)

def run_fastapi():
    """Executa o FastAPI em uma thread separada"""
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")

def run_frontend_server():
    """Executa o servidor de frontend"""
    with socketserver.TCPServer(("", 8000), CustomHandler) as httpd:
        print("🚀 Servidor frontend rodando em http://0.0.0.0:8000")
        print("📊 API backend rodando em http://127.0.0.1:8001")
        httpd.serve_forever()

if __name__ == "__main__":
    # Iniciar FastAPI em thread separada
    api_thread = threading.Thread(target=run_fastapi, daemon=True)
    api_thread.start()
    
    # Aguardar um pouco para o FastAPI inicializar
    import time
    time.sleep(2)
    
    # Iniciar servidor de frontend
    run_frontend_server()
