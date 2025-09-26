from fastapi import APIRouter
from .endpoints import transacoes, contas, processador_ia, investimentos, configuracoes

api_router = APIRouter()

# Incluir todos os roteadores dos endpoints
api_router.include_router(
    transacoes.router,
    prefix="/transacoes",
    tags=["Transações"]
)

api_router.include_router(
    contas.router,
    prefix="/contas",
    tags=["Contas"]
)

api_router.include_router(
    processador_ia.router,
    prefix="/processamento",
    tags=["Processamento IA"]
)

api_router.include_router(
    investimentos.router,
    prefix="/investimentos",
    tags=["Investimentos e Metas"]
)

api_router.include_router(
    configuracoes.router,
    prefix="/configuracoes",
    tags=["Configurações"]
)
