#!/usr/bin/env python3
"""
Wrapper para executar a aplicação FastAPI como se fosse Flask
para compatibilidade com o sistema de deploy
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
else:
    # Para deployment, exportar a aplicação
    application = app
