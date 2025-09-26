from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum
import uuid

class FormaPagamento(str, Enum):
    DINHEIRO = "dinheiro"
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    PIX = "pix"
    TRANSFERENCIA = "transferencia"
    BOLETO = "boleto"
    CONTA_CORRENTE = "conta_corrente"

class Gasto(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    descricao: str
    valor: float
    data: date
    categoria: str
    forma_pagamento: FormaPagamento
    conta_id: Optional[str] = None
    parcela_atual: Optional[int] = 1
    total_parcelas: Optional[int] = 1
    data_ultima_parcela: Optional[date] = None
    pensao_alimenticia: bool = False
    observacoes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class GastoCreate(BaseModel):
    descricao: str
    valor: float
    data: date
    categoria: str
    forma_pagamento: FormaPagamento
    conta_id: Optional[str] = None
    parcela_atual: Optional[int] = 1
    total_parcelas: Optional[int] = 1
    data_ultima_parcela: Optional[date] = None
    pensao_alimenticia: bool = False
    observacoes: Optional[str] = None

class GastoUpdate(BaseModel):
    descricao: Optional[str] = None
    valor: Optional[float] = None
    data: Optional[date] = None
    categoria: Optional[str] = None
    forma_pagamento: Optional[FormaPagamento] = None
    conta_id: Optional[str] = None
    parcela_atual: Optional[int] = None
    total_parcelas: Optional[int] = None
    data_ultima_parcela: Optional[date] = None
    pensao_alimenticia: Optional[bool] = None
    observacoes: Optional[str] = None

class Receita(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    descricao: str
    valor: float
    data: date
    categoria: str
    conta_id: Optional[str] = None
    forma_pagamento: Optional[str] = None
    observacoes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class ReceitaCreate(BaseModel):
    descricao: str
    valor: float
    data: date
    categoria: str
    conta_id: Optional[str] = None
    forma_pagamento: Optional[str] = None
    observacoes: Optional[str] = None

class ReceitaUpdate(BaseModel):
    descricao: Optional[str] = None
    valor: Optional[float] = None
    data: Optional[date] = None
    categoria: Optional[str] = None
    conta_id: Optional[str] = None
    forma_pagamento: Optional[str] = None
    observacoes: Optional[str] = None

class Categoria(BaseModel):
    id: str
    nome: str
    tipo: str  # "gasto" ou "receita"
    cor: str
    icone: str
    created_at: datetime
