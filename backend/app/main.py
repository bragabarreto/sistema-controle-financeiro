from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import logging
import sys
import os
from .core.config import settings
from .api.v1.api import api_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Criar instância da aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Sistema completo de controle financeiro com processamento de documentos via IA",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Incluir roteadores da API
app.include_router(api_router, prefix="/api/v1")

# Middleware para tratamento de erros
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Erro não tratado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )

# Endpoints de saúde e informações
@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Sistema de Controle Financeiro API",
        "version": settings.VERSION,
        "status": "online",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde"""
    try:
        # Verificar se o arquivo de dados está acessível
        from .services.servico_dados import servico_dados
        data = servico_dados.load_data()
        
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "data_file_accessible": True,
            "total_records": (
                len(data.get("gastos", [])) + 
                len(data.get("receitas", [])) + 
                len(data.get("contas", []))
            )
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )

@app.get("/api/v1/info")
async def api_info():
    """Informações detalhadas da API"""
    return {
        "api_name": settings.APP_NAME,
        "version": settings.VERSION,
        "debug_mode": settings.DEBUG,
        "endpoints": {
            "transacoes": "/api/v1/transacoes",
            "contas": "/api/v1/contas", 
            "processamento": "/api/v1/processamento",
            "investimentos": "/api/v1/investimentos",
            "configuracoes": "/api/v1/configuracoes"
        },
        "features": [
            "Controle de gastos e receitas",
            "Gestão de contas bancárias",
            "Processamento de contracheques via IA",
            "Processamento de extratos bancários via IA",
            "Processamento de extratos de cartão via IA",
            "Controle de investimentos",
            "Sistema de metas financeiras",
            "Backup e restore de dados",
            "Múltiplos provedores de IA (OpenAI, Anthropic, Gemini)"
        ]
    }

# Evento de inicialização
@app.on_event("startup")
async def startup_event():
    """Executado na inicialização da aplicação"""
    logger.info(f"🚀 Iniciando {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"📊 Modo debug: {settings.DEBUG}")
    logger.info(f"📁 Arquivo de dados: {settings.DATA_FILE_PATH}")
    
    # Verificar se o arquivo de dados existe e é acessível
    try:
        from .services.servico_dados import servico_dados
        data = servico_dados.load_data()
        logger.info(f"✅ Arquivo de dados carregado com sucesso")
        logger.info(f"📈 Total de registros: {len(data.get('gastos', [])) + len(data.get('receitas', []))}")
    except Exception as e:
        logger.error(f"❌ Erro ao carregar arquivo de dados: {str(e)}")

# Evento de encerramento
@app.on_event("shutdown")
async def shutdown_event():
    """Executado no encerramento da aplicação"""
    logger.info(f"🛑 Encerrando {settings.APP_NAME}")

# Servir arquivos estáticos do frontend (deve ser o último mount)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
