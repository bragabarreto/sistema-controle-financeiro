from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Dict, Any
import uuid
from datetime import datetime, date
from ....services.processamento_arquivos import processamento_arquivos
from ....services.servico_dados import servico_dados
from ....core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/contracheque/processar")
async def processar_contracheque(arquivo: UploadFile = File(...)):
    """Processa contracheque usando IA para extrair rubricas"""
    try:
        # Validar tipo de arquivo
        if arquivo.content_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de arquivo não suportado. Use: {', '.join(settings.ALLOWED_FILE_TYPES)}"
            )
        
        # Validar tamanho do arquivo
        file_content = await arquivo.read()
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo muito grande. Tamanho máximo: {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
        
        # Processar contracheque
        logger.info(f"Processando contracheque: {arquivo.filename}")
        dados_extraidos = await processamento_arquivos.processar_contracheque(
            file_content, arquivo.filename, arquivo.content_type
        )
        
        return {
            "message": "Contracheque processado com sucesso!",
            "arquivo_nome": arquivo.filename,
            "dados_extraidos": dados_extraidos
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no processamento do contracheque: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/contracheque/processar-detalhado")
async def processar_contracheque_detalhado(dados: Dict[str, Any], arquivo_nome: str = Form(...)):
    """Processa rubricas do contracheque e cria registros individuais"""
    try:
        logger.info("Iniciando processamento detalhado do contracheque...")
        
        transacoes_criadas = []
        
        # Processar créditos (receitas)
        rubricas_creditos = dados.get('rubricas_creditos', [])
        for rubrica in rubricas_creditos:
            descricao = rubrica.get('descricao', '')
            valor = float(rubrica.get('valor', 0))
            
            if valor <= 0:
                continue
            
            # Determinar categoria baseada na descrição
            categoria = _categorizar_rubrica_credito(descricao)
            
            # Criar receita
            receita_dict = {
                "id": str(uuid.uuid4()),
                "descricao": f"CONTRACHEQUE - {descricao}",
                "valor": valor,
                "data": date.today().isoformat(),
                "categoria": categoria,
                "conta_id": None,
                "observacoes": f"Importado de contracheque - {arquivo_nome}",
                "created_at": datetime.now().isoformat()
            }
            
            servico_dados.create_receita(receita_dict)
            transacoes_criadas.append({
                "tipo": "receita",
                "id": receita_dict["id"],
                "descricao": descricao,
                "categoria": categoria,
                "valor": valor
            })
        
        # Processar débitos (gastos)
        rubricas_debitos = dados.get('rubricas_debitos', [])
        for rubrica in rubricas_debitos:
            descricao = rubrica.get('descricao', '')
            valor = float(rubrica.get('valor', 0))
            
            if valor <= 0:
                continue
            
            # Determinar categoria baseada na descrição
            categoria = _categorizar_rubrica_debito(descricao)
            
            # Criar gasto
            gasto_dict = {
                "id": str(uuid.uuid4()),
                "descricao": f"CONTRACHEQUE - {descricao}",
                "valor": valor,
                "data": date.today().isoformat(),
                "categoria": categoria,
                "forma_pagamento": "conta_corrente",
                "conta_id": None,
                "observacoes": f"Importado de contracheque - {arquivo_nome}",
                "created_at": datetime.now().isoformat()
            }
            
            servico_dados.create_gasto(gasto_dict)
            transacoes_criadas.append({
                "tipo": "gasto",
                "id": gasto_dict["id"],
                "descricao": descricao,
                "categoria": categoria,
                "valor": valor
            })
        
        # Salvar histórico do contracheque processado
        contracheque_historico = {
            "id": str(uuid.uuid4()),
            "arquivo_nome": arquivo_nome,
            "empresa_pagadora": dados.get('empresa_pagadora', ''),
            "funcionario": dados.get('funcionario', ''),
            "competencia_mes": dados.get('competencia_mes', None),
            "competencia_ano": dados.get('competencia_ano', None),
            "valor_bruto_total": dados.get('valor_bruto_total', 0.0),
            "valor_descontos_total": dados.get('valor_descontos_total', 0.0),
            "valor_liquido_total": dados.get('valor_liquido_total', 0.0),
            "rubricas_creditos": rubricas_creditos,
            "rubricas_debitos": rubricas_debitos,
            "transacoes_criadas": transacoes_criadas,
            "data_processamento": date.today().isoformat(),
            "created_at": datetime.now().isoformat()
        }
        
        servico_dados.save_contracheque_processado(contracheque_historico)
        
        return {
            "message": "Contracheque processado com sucesso!",
            "arquivo_nome": arquivo_nome,
            "transacoes_criadas": len(transacoes_criadas),
            "valor_bruto": dados.get('valor_bruto_total', 0.0),
            "valor_liquido": dados.get('valor_liquido_total', 0.0),
            "empresa": dados.get('empresa_pagadora', ''),
            "competencia": f"{dados.get('competencia_mes', 0)}/{dados.get('competencia_ano', 0)}"
        }
        
    except Exception as e:
        logger.error(f"Erro no processamento detalhado do contracheque: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/extrato-bancario/processar")
async def processar_extrato_bancario(arquivo: UploadFile = File(...)):
    """Processa extrato bancário usando IA"""
    try:
        # Validar arquivo
        if arquivo.content_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de arquivo não suportado. Use: {', '.join(settings.ALLOWED_FILE_TYPES)}"
            )
        
        file_content = await arquivo.read()
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo muito grande. Tamanho máximo: {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
        
        # Processar extrato
        logger.info(f"Processando extrato bancário: {arquivo.filename}")
        dados_extraidos = await processamento_arquivos.processar_extrato_bancario(
            file_content, arquivo.filename, arquivo.content_type
        )
        
        return {
            "message": "Extrato bancário processado com sucesso!",
            "arquivo_nome": arquivo.filename,
            "dados_extraidos": dados_extraidos
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no processamento do extrato bancário: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/extrato-cartao/processar")
async def processar_extrato_cartao(arquivo: UploadFile = File(...)):
    """Processa extrato de cartão de crédito usando IA"""
    try:
        # Validar arquivo
        if arquivo.content_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de arquivo não suportado. Use: {', '.join(settings.ALLOWED_FILE_TYPES)}"
            )
        
        file_content = await arquivo.read()
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo muito grande. Tamanho máximo: {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
        
        # Processar extrato
        logger.info(f"Processando extrato de cartão: {arquivo.filename}")
        dados_extraidos = await processamento_arquivos.processar_extrato_cartao(
            file_content, arquivo.filename, arquivo.content_type
        )
        
        return {
            "message": "Extrato de cartão processado com sucesso!",
            "arquivo_nome": arquivo.filename,
            "dados_extraidos": dados_extraidos
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no processamento do extrato de cartão: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/contracheques/historico")
async def listar_contracheques():
    """Lista histórico de contracheques processados"""
    try:
        data = servico_dados.load_data()
        return data.get("contracheques_processados", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/extratos-bancarios/historico")
async def listar_extratos_bancarios():
    """Lista histórico de extratos bancários processados"""
    try:
        data = servico_dados.load_data()
        return data.get("extratos_bancarios_processados", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/extratos-cartao/historico")
async def listar_extratos_cartao():
    """Lista histórico de extratos de cartão processados"""
    try:
        data = servico_dados.load_data()
        return data.get("extratos_cartao_processados", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# === FUNÇÕES AUXILIARES ===

def _categorizar_rubrica_credito(descricao: str) -> str:
    """Categoriza rubrica de crédito baseada na descrição"""
    descricao_lower = descricao.lower()
    
    if any(termo in descricao_lower for termo in ['subsídio', 'salário', 'vencimento']):
        return "Salário"
    elif any(termo in descricao_lower for termo in ['substituição', 'adicional']):
        return "Adicionais"
    elif any(termo in descricao_lower for termo in ['gratificação', 'grat', 'gecj']):
        return "Gratificação"
    elif any(termo in descricao_lower for termo in ['auxílio', 'assistência', 'licença']):
        return "Verbas indenizatórias"
    elif any(termo in descricao_lower for termo in ['curso', 'concurso', 'palestra']):
        return "Aulas/Palestras"
    else:
        return "Outros"

def _categorizar_rubrica_debito(descricao: str) -> str:
    """Categoriza rubrica de débito baseada na descrição"""
    descricao_lower = descricao.lower()
    
    if any(termo in descricao_lower for termo in ['devolução', 'limite constitucional', 'abate']):
        return "Abate teto"
    elif any(termo in descricao_lower for termo in ['plano de saúde', 'saúde']):
        return "Saúde"
    elif any(termo in descricao_lower for termo in ['amatra', 'associação']):
        return "Associação"
    elif any(termo in descricao_lower for termo in ['empréstimo']):
        return "Empréstimos"
    elif any(termo in descricao_lower for termo in ['rpps', 'previdência pública']):
        return "Previdência pública"
    elif any(termo in descricao_lower for termo in ['funprespjud', 'previdência privada']):
        return "Previdência privada"
    elif any(termo in descricao_lower for termo in ['pensão alimentícia']):
        return "Pensão alimentícia"
    elif any(termo in descricao_lower for termo in ['imposto de renda', 'ir']):
        return "Impostos e taxas públicas"
    else:
        return "Outros"
