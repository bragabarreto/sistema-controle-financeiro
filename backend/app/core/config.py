import os
from typing import Optional

class Settings:
    # Configurações da aplicação
    APP_NAME: str = "Sistema de Controle Financeiro"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Configurações de CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://localhost:3000",
    ]
    
    # Configurações de arquivos
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list = [
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/jpg"
    ]
    
    # Configurações de IA
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    
    # Configurações de dados
    DATA_FILE_PATH: str = os.path.join(os.path.dirname(__file__), "..", "data", "schemas.json")
    
    # Configurações de upload
    UPLOAD_DIR: str = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")

settings = Settings()

# Criar diretório de uploads se não existir
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
