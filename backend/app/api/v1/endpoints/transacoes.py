from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date
from ....models.transacao import (
    Gasto, GastoCreate, GastoUpdate,
    Receita, ReceitaCreate, ReceitaUpdate,
    Categoria
)
from ....services.servico_dados import servico_dados
import uuid

router = APIRouter()

# === ENDPOINTS DE GASTOS ===

@router.get("/gastos", response_model=List[Gasto])
async def listar_gastos(
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    data_inicio: Optional[date] = Query(None, description="Data de início do período"),
    data_fim: Optional[date] = Query(None, description="Data de fim do período"),
    forma_pagamento: Optional[str] = Query(None, description="Filtrar por forma de pagamento")
):
    """Lista todos os gastos com filtros opcionais"""
    try:
        filtros = {}
        if categoria:
            filtros["categoria"] = categoria
        if data_inicio:
            filtros["data_inicio"] = data_inicio
        if data_fim:
            filtros["data_fim"] = data_fim
        if forma_pagamento:
            filtros["forma_pagamento"] = forma_pagamento
        
        gastos = servico_dados.get_gastos(filtros)
        return gastos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/gastos", response_model=Gasto)
async def criar_gasto(gasto: GastoCreate):
    """Cria um novo gasto"""
    try:
        gasto_dict = gasto.dict()
        gasto_dict["id"] = str(uuid.uuid4())
        
        # Converter date para string ISO
        if isinstance(gasto_dict.get("data"), date):
            gasto_dict["data"] = gasto_dict["data"].isoformat()
        if isinstance(gasto_dict.get("data_ultima_parcela"), date):
            gasto_dict["data_ultima_parcela"] = gasto_dict["data_ultima_parcela"].isoformat()
        
        gasto_criado = servico_dados.create_gasto(gasto_dict)
        return gasto_criado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/gastos/{gasto_id}", response_model=Gasto)
async def obter_gasto(gasto_id: str):
    """Obtém um gasto específico por ID"""
    try:
        gastos = servico_dados.get_gastos()
        gasto = next((g for g in gastos if g["id"] == gasto_id), None)
        
        if not gasto:
            raise HTTPException(status_code=404, detail="Gasto não encontrado")
        
        return gasto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/gastos/{gasto_id}", response_model=Gasto)
async def atualizar_gasto(gasto_id: str, gasto: GastoUpdate):
    """Atualiza um gasto existente"""
    try:
        gasto_dict = gasto.dict(exclude_unset=True)
        
        # Converter date para string ISO
        if isinstance(gasto_dict.get("data"), date):
            gasto_dict["data"] = gasto_dict["data"].isoformat()
        if isinstance(gasto_dict.get("data_ultima_parcela"), date):
            gasto_dict["data_ultima_parcela"] = gasto_dict["data_ultima_parcela"].isoformat()
        
        gasto_atualizado = servico_dados.update_gasto(gasto_id, gasto_dict)
        
        if not gasto_atualizado:
            raise HTTPException(status_code=404, detail="Gasto não encontrado")
        
        return gasto_atualizado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/gastos/{gasto_id}")
async def deletar_gasto(gasto_id: str):
    """Remove um gasto"""
    try:
        sucesso = servico_dados.delete_gasto(gasto_id)
        
        if not sucesso:
            raise HTTPException(status_code=404, detail="Gasto não encontrado")
        
        return {"message": "Gasto removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# === ENDPOINTS DE RECEITAS ===

@router.get("/receitas", response_model=List[Receita])
async def listar_receitas(
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    data_inicio: Optional[date] = Query(None, description="Data de início do período"),
    data_fim: Optional[date] = Query(None, description="Data de fim do período")
):
    """Lista todas as receitas com filtros opcionais"""
    try:
        filtros = {}
        if categoria:
            filtros["categoria"] = categoria
        if data_inicio:
            filtros["data_inicio"] = data_inicio
        if data_fim:
            filtros["data_fim"] = data_fim
        
        receitas = servico_dados.get_receitas(filtros)
        return receitas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/receitas", response_model=Receita)
async def criar_receita(receita: ReceitaCreate):
    """Cria uma nova receita"""
    try:
        receita_dict = receita.dict()
        receita_dict["id"] = str(uuid.uuid4())
        
        # Converter date para string ISO
        if isinstance(receita_dict.get("data"), date):
            receita_dict["data"] = receita_dict["data"].isoformat()
        
        receita_criada = servico_dados.create_receita(receita_dict)
        return receita_criada
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/receitas/{receita_id}", response_model=Receita)
async def obter_receita(receita_id: str):
    """Obtém uma receita específica por ID"""
    try:
        receitas = servico_dados.get_receitas()
        receita = next((r for r in receitas if r["id"] == receita_id), None)
        
        if not receita:
            raise HTTPException(status_code=404, detail="Receita não encontrada")
        
        return receita
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/receitas/{receita_id}", response_model=Receita)
async def atualizar_receita(receita_id: str, receita: ReceitaUpdate):
    """Atualiza uma receita existente"""
    try:
        receita_dict = receita.dict(exclude_unset=True)
        
        # Converter date para string ISO
        if isinstance(receita_dict.get("data"), date):
            receita_dict["data"] = receita_dict["data"].isoformat()
        
        receita_atualizada = servico_dados.update_receita(receita_id, receita_dict)
        
        if not receita_atualizada:
            raise HTTPException(status_code=404, detail="Receita não encontrada")
        
        return receita_atualizada
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/receitas/{receita_id}")
async def deletar_receita(receita_id: str):
    """Remove uma receita"""
    try:
        sucesso = servico_dados.delete_receita(receita_id)
        
        if not sucesso:
            raise HTTPException(status_code=404, detail="Receita não encontrada")
        
        return {"message": "Receita removida com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# === ENDPOINTS DE CATEGORIAS ===

@router.get("/categorias")
async def listar_categorias():
    """Lista todas as categorias de gastos e receitas"""
    try:
        categorias = servico_dados.get_categorias()
        return categorias
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# === ENDPOINTS DE RELATÓRIOS ===

@router.get("/relatorios/resumo-mensal")
async def resumo_mensal(
    ano: int = Query(..., description="Ano do relatório"),
    mes: int = Query(..., description="Mês do relatório (1-12)")
):
    """Gera resumo mensal de gastos e receitas"""
    try:
        # Filtrar transações do mês
        data_inicio = f"{ano}-{mes:02d}-01"
        if mes == 12:
            data_fim = f"{ano + 1}-01-01"
        else:
            data_fim = f"{ano}-{mes + 1:02d}-01"
        
        gastos = servico_dados.get_gastos({"data_inicio": data_inicio, "data_fim": data_fim})
        receitas = servico_dados.get_receitas({"data_inicio": data_inicio, "data_fim": data_fim})
        
        # Calcular totais
        total_gastos = sum(float(g.get("valor", 0)) for g in gastos)
        total_receitas = sum(float(r.get("valor", 0)) for r in receitas)
        saldo = total_receitas - total_gastos
        
        # Agrupar por categoria
        gastos_por_categoria = {}
        for gasto in gastos:
            categoria = gasto.get("categoria", "Outros")
            if categoria not in gastos_por_categoria:
                gastos_por_categoria[categoria] = 0
            gastos_por_categoria[categoria] += float(gasto.get("valor", 0))
        
        receitas_por_categoria = {}
        for receita in receitas:
            categoria = receita.get("categoria", "Outros")
            if categoria not in receitas_por_categoria:
                receitas_por_categoria[categoria] = 0
            receitas_por_categoria[categoria] += float(receita.get("valor", 0))
        
        return {
            "periodo": f"{mes:02d}/{ano}",
            "total_gastos": round(total_gastos, 2),
            "total_receitas": round(total_receitas, 2),
            "saldo": round(saldo, 2),
            "gastos_por_categoria": gastos_por_categoria,
            "receitas_por_categoria": receitas_por_categoria,
            "quantidade_transacoes": len(gastos) + len(receitas)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
