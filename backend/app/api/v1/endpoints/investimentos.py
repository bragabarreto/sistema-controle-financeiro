from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date
from ....models.investimento import (
    Investimento, InvestimentoCreate, InvestimentoUpdate,
    Meta, MetaCreate, MetaUpdate
)
from ....services.servico_dados import servico_dados
import uuid

router = APIRouter()

# === ENDPOINTS DE INVESTIMENTOS ===

@router.get("/investimentos", response_model=List[Investimento])
async def listar_investimentos(
    ativo: Optional[bool] = Query(None, description="Filtrar por investimentos ativos"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de investimento")
):
    """Lista todos os investimentos com filtros opcionais"""
    try:
        investimentos = servico_dados.get_investimentos()
        
        # Aplicar filtros
        if ativo is not None:
            investimentos = [i for i in investimentos if i.get("ativo") == ativo]
        
        if tipo:
            investimentos = [i for i in investimentos if i.get("tipo_investimento") == tipo]
        
        return investimentos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/investimentos", response_model=Investimento)
async def criar_investimento(investimento: InvestimentoCreate):
    """Cria um novo investimento"""
    try:
        investimento_dict = investimento.dict()
        investimento_dict["id"] = str(uuid.uuid4())
        
        # Converter date para string ISO
        if isinstance(investimento_dict.get("data_aplicacao"), date):
            investimento_dict["data_aplicacao"] = investimento_dict["data_aplicacao"].isoformat()
        
        # Se valor_atual não foi fornecido, usar valor_inicial
        if not investimento_dict.get("valor_atual"):
            investimento_dict["valor_atual"] = investimento_dict["valor_inicial"]
        
        investimento_criado = servico_dados.create_investimento(investimento_dict)
        return investimento_criado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/investimentos/{investimento_id}", response_model=Investimento)
async def obter_investimento(investimento_id: str):
    """Obtém um investimento específico por ID"""
    try:
        investimentos = servico_dados.get_investimentos()
        investimento = next((i for i in investimentos if i["id"] == investimento_id), None)
        
        if not investimento:
            raise HTTPException(status_code=404, detail="Investimento não encontrado")
        
        return investimento
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/investimentos/{investimento_id}", response_model=Investimento)
async def atualizar_investimento(investimento_id: str, investimento: InvestimentoUpdate):
    """Atualiza um investimento existente"""
    try:
        data = servico_dados.load_data()
        investimentos = data.get("investimentos", [])
        
        for i, inv in enumerate(investimentos):
            if inv.get("id") == investimento_id:
                investimento_dict = investimento.dict(exclude_unset=True)
                
                # Converter date para string ISO
                if isinstance(investimento_dict.get("data_aplicacao"), date):
                    investimento_dict["data_aplicacao"] = investimento_dict["data_aplicacao"].isoformat()
                
                investimentos[i].update(investimento_dict)
                servico_dados.save_data(data)
                return investimentos[i]
        
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/investimentos/{investimento_id}")
async def deletar_investimento(investimento_id: str):
    """Remove um investimento"""
    try:
        data = servico_dados.load_data()
        investimentos = data.get("investimentos", [])
        
        for i, inv in enumerate(investimentos):
            if inv.get("id") == investimento_id:
                del investimentos[i]
                servico_dados.save_data(data)
                return {"message": "Investimento removido com sucesso"}
        
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/investimentos/resumo")
async def resumo_investimentos():
    """Gera resumo dos investimentos"""
    try:
        investimentos = servico_dados.get_investimentos()
        investimentos_ativos = [i for i in investimentos if i.get("ativo", True)]
        
        # Calcular totais
        valor_total_aplicado = sum(float(i.get("valor_inicial", 0)) for i in investimentos_ativos)
        valor_total_atual = sum(float(i.get("valor_atual", 0)) for i in investimentos_ativos)
        
        # Calcular rentabilidade
        rentabilidade_total = valor_total_atual - valor_total_aplicado if valor_total_aplicado > 0 else 0
        percentual_rentabilidade = (rentabilidade_total / valor_total_aplicado * 100) if valor_total_aplicado > 0 else 0
        
        # Agrupar por tipo
        por_tipo = {}
        for inv in investimentos_ativos:
            tipo = inv.get("tipo_investimento", "outros")
            if tipo not in por_tipo:
                por_tipo[tipo] = {
                    "quantidade": 0,
                    "valor_aplicado": 0,
                    "valor_atual": 0
                }
            
            por_tipo[tipo]["quantidade"] += 1
            por_tipo[tipo]["valor_aplicado"] += float(inv.get("valor_inicial", 0))
            por_tipo[tipo]["valor_atual"] += float(inv.get("valor_atual", 0))
        
        # Calcular rentabilidade por tipo
        for tipo_data in por_tipo.values():
            rentabilidade = tipo_data["valor_atual"] - tipo_data["valor_aplicado"]
            tipo_data["rentabilidade"] = round(rentabilidade, 2)
            tipo_data["percentual"] = round(
                (rentabilidade / tipo_data["valor_aplicado"] * 100) if tipo_data["valor_aplicado"] > 0 else 0, 2
            )
        
        return {
            "total_investimentos": len(investimentos_ativos),
            "valor_total_aplicado": round(valor_total_aplicado, 2),
            "valor_total_atual": round(valor_total_atual, 2),
            "rentabilidade_total": round(rentabilidade_total, 2),
            "percentual_rentabilidade": round(percentual_rentabilidade, 2),
            "por_tipo": por_tipo
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# === ENDPOINTS DE METAS ===

@router.get("/metas", response_model=List[Meta])
async def listar_metas(
    ativa: Optional[bool] = Query(None, description="Filtrar por metas ativas")
):
    """Lista todas as metas com filtros opcionais"""
    try:
        data = servico_dados.load_data()
        metas = data.get("metas", [])
        
        if ativa is not None:
            metas = [m for m in metas if m.get("ativa") == ativa]
        
        return metas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/metas", response_model=Meta)
async def criar_meta(meta: MetaCreate):
    """Cria uma nova meta"""
    try:
        meta_dict = meta.dict()
        meta_dict["id"] = str(uuid.uuid4())
        meta_dict["valor_atual"] = 0.0
        meta_dict["ativa"] = True
        
        # Converter dates para string ISO
        if isinstance(meta_dict.get("data_inicio"), date):
            meta_dict["data_inicio"] = meta_dict["data_inicio"].isoformat()
        if isinstance(meta_dict.get("data_objetivo"), date):
            meta_dict["data_objetivo"] = meta_dict["data_objetivo"].isoformat()
        
        data = servico_dados.load_data()
        meta_dict["created_at"] = datetime.now().isoformat()
        data["metas"].append(meta_dict)
        servico_dados.save_data(data)
        
        return meta_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/metas/{meta_id}", response_model=Meta)
async def obter_meta(meta_id: str):
    """Obtém uma meta específica por ID"""
    try:
        data = servico_dados.load_data()
        metas = data.get("metas", [])
        meta = next((m for m in metas if m["id"] == meta_id), None)
        
        if not meta:
            raise HTTPException(status_code=404, detail="Meta não encontrada")
        
        return meta
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/metas/{meta_id}", response_model=Meta)
async def atualizar_meta(meta_id: str, meta: MetaUpdate):
    """Atualiza uma meta existente"""
    try:
        data = servico_dados.load_data()
        metas = data.get("metas", [])
        
        for i, m in enumerate(metas):
            if m.get("id") == meta_id:
                meta_dict = meta.dict(exclude_unset=True)
                
                # Converter dates para string ISO
                if isinstance(meta_dict.get("data_inicio"), date):
                    meta_dict["data_inicio"] = meta_dict["data_inicio"].isoformat()
                if isinstance(meta_dict.get("data_objetivo"), date):
                    meta_dict["data_objetivo"] = meta_dict["data_objetivo"].isoformat()
                
                metas[i].update(meta_dict)
                servico_dados.save_data(data)
                return metas[i]
        
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/metas/{meta_id}")
async def deletar_meta(meta_id: str):
    """Remove uma meta"""
    try:
        data = servico_dados.load_data()
        metas = data.get("metas", [])
        
        for i, m in enumerate(metas):
            if m.get("id") == meta_id:
                del metas[i]
                servico_dados.save_data(data)
                return {"message": "Meta removida com sucesso"}
        
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/metas/{meta_id}/contribuir")
async def contribuir_meta(meta_id: str, valor: float):
    """Adiciona valor à meta"""
    try:
        if valor <= 0:
            raise HTTPException(status_code=400, detail="Valor deve ser positivo")
        
        data = servico_dados.load_data()
        metas = data.get("metas", [])
        
        for i, m in enumerate(metas):
            if m.get("id") == meta_id:
                valor_atual = float(m.get("valor_atual", 0))
                metas[i]["valor_atual"] = valor_atual + valor
                servico_dados.save_data(data)
                
                # Verificar se a meta foi atingida
                valor_objetivo = float(m.get("valor_objetivo", 0))
                if metas[i]["valor_atual"] >= valor_objetivo:
                    return {
                        "message": "Parabéns! Meta atingida!",
                        "meta_atingida": True,
                        "valor_atual": metas[i]["valor_atual"],
                        "valor_objetivo": valor_objetivo
                    }
                
                return {
                    "message": "Contribuição adicionada com sucesso!",
                    "meta_atingida": False,
                    "valor_atual": metas[i]["valor_atual"],
                    "valor_objetivo": valor_objetivo,
                    "percentual_atingido": round((metas[i]["valor_atual"] / valor_objetivo * 100), 2)
                }
        
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/metas/resumo")
async def resumo_metas():
    """Gera resumo das metas"""
    try:
        data = servico_dados.load_data()
        metas = data.get("metas", [])
        metas_ativas = [m for m in metas if m.get("ativa", True)]
        
        total_metas = len(metas_ativas)
        metas_atingidas = len([m for m in metas_ativas if float(m.get("valor_atual", 0)) >= float(m.get("valor_objetivo", 0))])
        
        valor_total_objetivo = sum(float(m.get("valor_objetivo", 0)) for m in metas_ativas)
        valor_total_atual = sum(float(m.get("valor_atual", 0)) for m in metas_ativas)
        
        percentual_geral = (valor_total_atual / valor_total_objetivo * 100) if valor_total_objetivo > 0 else 0
        
        return {
            "total_metas": total_metas,
            "metas_atingidas": metas_atingidas,
            "metas_pendentes": total_metas - metas_atingidas,
            "valor_total_objetivo": round(valor_total_objetivo, 2),
            "valor_total_atual": round(valor_total_atual, 2),
            "percentual_geral": round(percentual_geral, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
