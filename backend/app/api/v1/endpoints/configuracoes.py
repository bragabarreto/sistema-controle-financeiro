from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ....models.extrato import LLMConfigCreate, LLMConfigInDB
from ....services.servico_dados import servico_dados
import uuid
from datetime import datetime
import json

router = APIRouter()

# === ENDPOINTS DE CONFIGURAÇÕES LLM ===

@router.get("/llm-configs", response_model=List[LLMConfigInDB])
async def listar_configs_llm():
    """Lista todas as configurações de LLM"""
    try:
        configs = servico_dados.get_llm_configs()
        return configs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/llm-configs", response_model=LLMConfigInDB)
async def criar_config_llm(config: LLMConfigCreate):
    """Cria uma nova configuração de LLM"""
    try:
        config_dict = config.dict()
        config_dict["id"] = str(uuid.uuid4())
        
        # Criar preview da chave API (primeiros 8 e últimos 4 caracteres)
        api_key = config_dict["api_key"]
        if len(api_key) > 12:
            config_dict["api_key_preview"] = f"{api_key[:8]}...{api_key[-4:]}"
        else:
            config_dict["api_key_preview"] = f"{api_key[:4]}...{api_key[-2:]}"
        
        config_dict["is_active"] = True
        config_dict["created_at"] = datetime.now().isoformat()
        
        config_criada = servico_dados.save_llm_config(config_dict)
        return config_criada
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/llm-configs/{config_id}")
async def deletar_config_llm(config_id: str):
    """Remove uma configuração de LLM"""
    try:
        data = servico_dados.load_data()
        configs = data.get("llm_configs", [])
        
        for i, config in enumerate(configs):
            if config.get("id") == config_id:
                del configs[i]
                servico_dados.save_data(data)
                return {"message": "Configuração removida com sucesso"}
        
        raise HTTPException(status_code=404, detail="Configuração não encontrada")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/llm-configs/{config_id}/toggle")
async def alternar_config_llm(config_id: str):
    """Ativa/desativa uma configuração de LLM"""
    try:
        data = servico_dados.load_data()
        configs = data.get("llm_configs", [])
        
        for i, config in enumerate(configs):
            if config.get("id") == config_id:
                configs[i]["is_active"] = not configs[i].get("is_active", True)
                servico_dados.save_data(data)
                
                status = "ativada" if configs[i]["is_active"] else "desativada"
                return {"message": f"Configuração {status} com sucesso"}
        
        raise HTTPException(status_code=404, detail="Configuração não encontrada")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# === ENDPOINTS DE BACKUP E RESTORE ===

@router.get("/backup/export")
async def exportar_dados():
    """Exporta todos os dados do sistema"""
    try:
        data = servico_dados.load_data()
        
        # Remover chaves API sensíveis do backup
        backup_data = data.copy()
        if "llm_configs" in backup_data:
            for config in backup_data["llm_configs"]:
                if "api_key" in config:
                    del config["api_key"]
        
        # Atualizar metadata do backup
        backup_data["backup_metadata"]["export_date"] = datetime.now().isoformat()
        backup_data["backup_metadata"]["export_version"] = "1.0.0"
        
        return {
            "message": "Dados exportados com sucesso",
            "data": backup_data,
            "export_info": {
                "total_gastos": len(backup_data.get("gastos", [])),
                "total_receitas": len(backup_data.get("receitas", [])),
                "total_contas": len(backup_data.get("contas", [])),
                "total_investimentos": len(backup_data.get("investimentos", [])),
                "export_date": backup_data["backup_metadata"]["export_date"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/backup/import")
async def importar_dados(backup_data: Dict[str, Any]):
    """Importa dados para o sistema"""
    try:
        # Validar estrutura básica do backup
        required_keys = ["gastos", "receitas", "contas", "categorias"]
        for key in required_keys:
            if key not in backup_data:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Backup inválido: chave '{key}' não encontrada"
                )
        
        # Fazer backup dos dados atuais antes de importar
        current_data = servico_dados.load_data()
        backup_filename = f"backup_pre_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Salvar dados importados
        backup_data["backup_metadata"]["import_date"] = datetime.now().isoformat()
        backup_data["backup_metadata"]["previous_backup"] = backup_filename
        
        servico_dados.save_data(backup_data)
        
        return {
            "message": "Dados importados com sucesso",
            "import_info": {
                "total_gastos": len(backup_data.get("gastos", [])),
                "total_receitas": len(backup_data.get("receitas", [])),
                "total_contas": len(backup_data.get("contas", [])),
                "total_investimentos": len(backup_data.get("investimentos", [])),
                "import_date": backup_data["backup_metadata"]["import_date"],
                "backup_anterior": backup_filename
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/backup/info")
async def info_backup():
    """Obtém informações sobre o backup atual"""
    try:
        data = servico_dados.load_data()
        backup_metadata = data.get("backup_metadata", {})
        
        # Calcular estatísticas
        stats = {
            "total_gastos": len(data.get("gastos", [])),
            "total_receitas": len(data.get("receitas", [])),
            "total_contas": len(data.get("contas", [])),
            "total_investimentos": len(data.get("investimentos", [])),
            "total_contracheques": len(data.get("contracheques_processados", [])),
            "total_extratos_bancarios": len(data.get("extratos_bancarios_processados", [])),
            "total_extratos_cartao": len(data.get("extratos_cartao_processados", [])),
            "total_metas": len(data.get("metas", [])),
            "total_configs_llm": len(data.get("llm_configs", []))
        }
        
        return {
            "backup_metadata": backup_metadata,
            "estatisticas": stats,
            "tamanho_dados": len(json.dumps(data, default=str))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# === ENDPOINTS DE CONFIGURAÇÕES GERAIS ===

@router.get("/sistema/status")
async def status_sistema():
    """Obtém status geral do sistema"""
    try:
        data = servico_dados.load_data()
        
        # Verificar configurações de IA
        configs_llm = data.get("llm_configs", [])
        configs_ativas = [c for c in configs_llm if c.get("is_active", True)]
        
        # Calcular estatísticas de uso
        total_transacoes = len(data.get("gastos", [])) + len(data.get("receitas", []))
        total_processamentos = (
            len(data.get("contracheques_processados", [])) +
            len(data.get("extratos_bancarios_processados", [])) +
            len(data.get("extratos_cartao_processados", []))
        )
        
        return {
            "sistema": {
                "versao": "1.0.0",
                "status": "online",
                "data_inicializacao": data.get("backup_metadata", {}).get("version", "1.0.0")
            },
            "configuracoes_ia": {
                "total_configs": len(configs_llm),
                "configs_ativas": len(configs_ativas),
                "provedores_disponiveis": list(set(c.get("provider") for c in configs_ativas))
            },
            "estatisticas_uso": {
                "total_transacoes": total_transacoes,
                "total_contas": len(data.get("contas", [])),
                "total_investimentos": len(data.get("investimentos", [])),
                "total_processamentos_ia": total_processamentos
            },
            "ultimo_backup": data.get("backup_metadata", {}).get("last_backup")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/sistema/reset")
async def reset_sistema():
    """Reseta o sistema para o estado inicial (CUIDADO!)"""
    try:
        # Fazer backup antes do reset
        current_data = servico_dados.load_data()
        backup_filename = f"backup_pre_reset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Recriar arquivo inicial
        servico_dados._create_initial_data_file()
        
        return {
            "message": "Sistema resetado com sucesso",
            "warning": "Todos os dados foram removidos",
            "backup_criado": backup_filename,
            "data_reset": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
