from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid

class TipoConta(str, Enum):
    CONTA_CORRENTE = "conta_corrente"
    CONTA_POUPANCA = "conta_poupanca"
    CARTAO_CREDITO = "cartao_credito"
    INVESTIMENTO = "investimento"

class Conta(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nome: str
    tipo_conta: TipoConta
    banco: Optional[str] = None
    numero_final: Optional[str] = None
    limite_credito: Optional[float] = None
    saldo_atual: float = 0.0
    eh_conta_salario: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

class ContaCreate(BaseModel):
    nome: str
    tipo_conta: TipoConta
    banco: Optional[str] = None
    numero_final: Optional[str] = None
    limite_credito: Optional[float] = None
    saldo_atual: float = 0.0
    eh_conta_salario: bool = False

class ContaUpdate(BaseModel):
    nome: Optional[str] = None
    tipo_conta: Optional[TipoConta] = None
    banco: Optional[str] = None
    numero_final: Optional[str] = None
    limite_credito: Optional[float] = None
    saldo_atual: Optional[float] = None
    eh_conta_salario: Optional[bool] = None
