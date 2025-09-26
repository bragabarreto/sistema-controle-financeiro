from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum
import uuid

class TipoExtrato(str, Enum):
    EXTRATO_BANCARIO = "extrato_bancario"
    EXTRATO_CARTAO_CREDITO = "extrato_cartao_credito"
    CONTRACHEQUE = "contracheque"

class TransacaoExtrato(BaseModel):
    data: str
    descricao: str
    valor: float
    tipo: str  # "debito" ou "credito"
    categoria_sugerida: str
    conta_identificada: Optional[str] = None
    parcela: Optional[str] = "1/1"

class ExtratoBancarioProcessado(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    arquivo_nome: str
    banco: Optional[str] = None
    conta: Optional[str] = None
    periodo_inicio: Optional[str] = None
    periodo_fim: Optional[str] = None
    saldo_inicial: Optional[float] = None
    saldo_final: Optional[float] = None
    transacoes: List[TransacaoExtrato] = []
    total_debitos: float = 0.0
    total_creditos: float = 0.0
    total_transacoes: int = 0
    data_processamento: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)

class ExtratoCartaoProcessado(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    arquivo_nome: str
    bandeira_cartao: Optional[str] = None
    numero_final_cartao: Optional[str] = None
    periodo_inicio: Optional[str] = None
    periodo_fim: Optional[str] = None
    valor_fatura: Optional[float] = None
    data_vencimento: Optional[str] = None
    transacoes: List[TransacaoExtrato] = []
    total_gastos: float = 0.0
    total_transacoes: int = 0
    data_processamento: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)

class RubricaContracheque(BaseModel):
    descricao: str
    valor: float

class ContrachequeProcessado(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    arquivo_nome: str
    empresa_pagadora: Optional[str] = None
    funcionario: Optional[str] = None
    competencia_mes: Optional[int] = None
    competencia_ano: Optional[int] = None
    data_processamento: date = Field(default_factory=date.today)
    data_previsao_credito: Optional[date] = None
    valor_bruto_total: float = 0.0
    valor_descontos_total: float = 0.0
    valor_liquido_total: float = 0.0
    rubricas_creditos: List[RubricaContracheque] = []
    rubricas_debitos: List[RubricaContracheque] = []
    transacoes_criadas: List[dict] = []
    created_at: datetime = Field(default_factory=datetime.now)

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"

class LLMConfigCreate(BaseModel):
    provider: LLMProvider
    model: str
    api_key: str

class LLMConfigInDB(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provider: LLMProvider
    model: str
    api_key_preview: str
    api_key: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
