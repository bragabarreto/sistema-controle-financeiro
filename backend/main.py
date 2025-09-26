#!/usr/bin/env python3
"""
Ponto de entrada principal para deploy da aplicação
"""

from app.main import app

# Para compatibilidade com sistemas de deploy Flask
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
