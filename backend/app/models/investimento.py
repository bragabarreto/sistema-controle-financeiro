from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum
import uuid

class TipoOperacaoInvestimento(str, Enum):
    APLICACAO = "aplicacao"
    RESGATE = "resgate"

class TipoInvestimento(str, Enum):
    POUPANCA = "poupanca"
    CDB = "cdb"
    LCI_LCA = "lci_lca"
    TESOURO_DIRETO = "tesouro_direto"
    FUNDOS = "fundos"
    ACOES = "acoes"
    FIIS = "fiis"
    CRIPTOMOEDAS = "criptomoedas"
    OUTROS = "outros"

class Investimento(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nome: str
    tipo_investimento: TipoInvestimento
    valor_inicial: float
    valor_atual: Optional[float] = None
    data_aplicacao: date
    conta_origem_id: Optional[str] = None
    conta_destino_id: Optional[str] = None
    rentabilidade_mes: Optional[float] = None
    observacoes: Optional[str] = None
    ativo: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

class InvestimentoCreate(BaseModel):
    nome: str
    tipo_investimento: TipoInvestimento
    valor_inicial: float
    data_aplicacao: date
    conta_origem_id: Optional[str] = None
    conta_destino_id: Optional[str] = None
    rentabilidade_mes: Optional[float] = None
    observacoes: Optional[str] = None

class InvestimentoUpdate(BaseModel):
    nome: Optional[str] = None
    tipo_investimento: Optional[TipoInvestimento] = None
    valor_inicial: Optional[float] = None
    valor_atual: Optional[float] = None
    data_aplicacao: Optional[date] = None
    conta_origem_id: Optional[str] = None
    conta_destino_id: Optional[str] = None
    rentabilidade_mes: Optional[float] = None
    observacoes: Optional[str] = None
    ativo: Optional[bool] = None

class Meta(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nome: str
    valor_objetivo: float
    valor_atual: float = 0.0
    data_inicio: date
    data_objetivo: date
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    ativa: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

class MetaCreate(BaseModel):
    nome: str
    valor_objetivo: float
    data_inicio: date
    data_objetivo: date
    categoria: Optional[str] = None
    descricao: Optional[str] = None

class MetaUpdate(BaseModel):
    nome: Optional[str] = None
    valor_objetivo: Optional[float] = None
    valor_atual: Optional[float] = None
    data_inicio: Optional[date] = None
    data_objetivo: Optional[date] = None
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    ativa: Optional[bool] = None
