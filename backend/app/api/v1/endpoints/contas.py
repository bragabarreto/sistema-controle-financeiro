from fastapi import APIRouter, HTTPException
from typing import List
from ....models.conta import Conta, ContaCreate, ContaUpdate
from ....services.servico_dados import servico_dados
import uuid

router = APIRouter()

@router.get("/contas", response_model=List[Conta])
async def listar_contas():
    """Lista todas as contas"""
    try:
        contas = servico_dados.get_contas()
        return contas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/contas", response_model=Conta)
async def criar_conta(conta: ContaCreate):
    """Cria uma nova conta"""
    try:
        conta_dict = conta.dict()
        conta_dict["id"] = str(uuid.uuid4())
        
        conta_criada = servico_dados.create_conta(conta_dict)
        return conta_criada
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/contas/{conta_id}", response_model=Conta)
async def obter_conta(conta_id: str):
    """Obtém uma conta específica por ID"""
    try:
        contas = servico_dados.get_contas()
        conta = next((c for c in contas if c["id"] == conta_id), None)
        
        if not conta:
            raise HTTPException(status_code=404, detail="Conta não encontrada")
        
        return conta
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/contas/{conta_id}", response_model=Conta)
async def atualizar_conta(conta_id: str, conta: ContaUpdate):
    """Atualiza uma conta existente"""
    try:
        conta_dict = conta.dict(exclude_unset=True)
        conta_atualizada = servico_dados.update_conta(conta_id, conta_dict)
        
        if not conta_atualizada:
            raise HTTPException(status_code=404, detail="Conta não encontrada")
        
        return conta_atualizada
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/contas/{conta_id}")
async def deletar_conta(conta_id: str):
    """Remove uma conta"""
    try:
        # Verificar se a conta está sendo usada em transações
        gastos = servico_dados.get_gastos()
        receitas = servico_dados.get_receitas()
        
        conta_em_uso = any(g.get("conta_id") == conta_id for g in gastos) or \
                      any(r.get("conta_id") == conta_id for r in receitas)
        
        if conta_em_uso:
            raise HTTPException(
                status_code=400, 
                detail="Não é possível excluir conta que possui transações associadas"
            )
        
        sucesso = servico_dados.delete_conta(conta_id)
        
        if not sucesso:
            raise HTTPException(status_code=404, detail="Conta não encontrada")
        
        return {"message": "Conta removida com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/contas/{conta_id}/saldo")
async def calcular_saldo_conta(conta_id: str):
    """Calcula o saldo atual de uma conta baseado nas transações"""
    try:
        # Verificar se a conta existe
        contas = servico_dados.get_contas()
        conta = next((c for c in contas if c["id"] == conta_id), None)
        
        if not conta:
            raise HTTPException(status_code=404, detail="Conta não encontrada")
        
        # Buscar transações da conta
        gastos = servico_dados.get_gastos()
        receitas = servico_dados.get_receitas()
        
        gastos_conta = [g for g in gastos if g.get("conta_id") == conta_id]
        receitas_conta = [r for r in receitas if r.get("conta_id") == conta_id]
        
        # Calcular saldo
        total_gastos = sum(float(g.get("valor", 0)) for g in gastos_conta)
        total_receitas = sum(float(r.get("valor", 0)) for r in receitas_conta)
        
        saldo_inicial = float(conta.get("saldo_atual", 0))
        saldo_calculado = saldo_inicial + total_receitas - total_gastos
        
        return {
            "conta_id": conta_id,
            "nome_conta": conta.get("nome"),
            "saldo_inicial": round(saldo_inicial, 2),
            "total_receitas": round(total_receitas, 2),
            "total_gastos": round(total_gastos, 2),
            "saldo_atual": round(saldo_calculado, 2),
            "quantidade_transacoes": len(gastos_conta) + len(receitas_conta)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/contas/{conta_id}/extrato")
async def extrato_conta(conta_id: str):
    """Gera extrato de uma conta com todas as transações"""
    try:
        # Verificar se a conta existe
        contas = servico_dados.get_contas()
        conta = next((c for c in contas if c["id"] == conta_id), None)
        
        if not conta:
            raise HTTPException(status_code=404, detail="Conta não encontrada")
        
        # Buscar transações da conta
        gastos = servico_dados.get_gastos()
        receitas = servico_dados.get_receitas()
        
        gastos_conta = [
            {
                **g,
                "tipo_transacao": "gasto",
                "valor_movimento": -float(g.get("valor", 0))
            }
            for g in gastos if g.get("conta_id") == conta_id
        ]
        
        receitas_conta = [
            {
                **r,
                "tipo_transacao": "receita",
                "valor_movimento": float(r.get("valor", 0))
            }
            for r in receitas if r.get("conta_id") == conta_id
        ]
        
        # Combinar e ordenar por data
        todas_transacoes = gastos_conta + receitas_conta
        todas_transacoes.sort(key=lambda x: x.get("data", ""), reverse=True)
        
        # Calcular saldo
        saldo_inicial = float(conta.get("saldo_atual", 0))
        total_receitas = sum(float(r.get("valor", 0)) for r in receitas_conta)
        total_gastos = sum(float(g.get("valor", 0)) for g in gastos_conta)
        saldo_atual = saldo_inicial + total_receitas - total_gastos
        
        return {
            "conta": conta,
            "saldo_inicial": round(saldo_inicial, 2),
            "saldo_atual": round(saldo_atual, 2),
            "total_receitas": round(total_receitas, 2),
            "total_gastos": round(total_gastos, 2),
            "transacoes": todas_transacoes,
            "quantidade_transacoes": len(todas_transacoes)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
