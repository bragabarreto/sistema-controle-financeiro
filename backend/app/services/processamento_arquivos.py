import base64
import json
import logging
import fitz  # PyMuPDF
from typing import Dict, Any, Optional, List
from datetime import datetime, date
import uuid
import os
import openai
import anthropic
import google.generativeai as genai
from ..core.config import settings

logger = logging.getLogger(__name__)

class ProcessamentoArquivos:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        # Configurar clientes de IA se as chaves estiverem disponíveis
        if settings.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
    
    def _extrair_texto_pdf(self, file_content: bytes) -> str:
        """Extrai texto de um arquivo PDF"""
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            texto_completo = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                texto_completo += page.get_text()
            
            doc.close()
            return texto_completo
        except Exception as e:
            logger.error(f"Erro ao extrair texto do PDF: {e}")
            raise Exception(f"Erro ao processar PDF: {e}")
    
    async def _chamar_openai(self, messages: List[str], model: str = "gpt-4o") -> str:
        """Chama a API da OpenAI"""
        if not self.openai_client:
            raise Exception("Cliente OpenAI não configurado")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": messages[0]},
                    {"role": "user", "content": messages[1]}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Erro na chamada OpenAI: {e}")
            raise Exception(f"Erro na API OpenAI: {e}")
    
    async def _chamar_anthropic(self, messages: List[str], model: str = "claude-3-sonnet-20240229") -> str:
        """Chama a API da Anthropic"""
        if not self.anthropic_client:
            raise Exception("Cliente Anthropic não configurado")
        
        try:
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=4000,
                temperature=0.1,
                system=messages[0],
                messages=[
                    {"role": "user", "content": messages[1]}
                ]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Erro na chamada Anthropic: {e}")
            raise Exception(f"Erro na API Anthropic: {e}")
    
    async def _chamar_gemini(self, messages: List[str], model: str = "gemini-1.5-pro") -> str:
        """Chama a API do Google Gemini"""
        if not settings.GOOGLE_API_KEY:
            raise Exception("Cliente Gemini não configurado")
        
        try:
            model_instance = genai.GenerativeModel(model)
            prompt = f"{messages[0]}\n\n{messages[1]}"
            
            response = model_instance.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=4000,
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Erro na chamada Gemini: {e}")
            raise Exception(f"Erro na API Gemini: {e}")
    
    async def _chamar_llm(self, messages: List[str], provider: str = "openai") -> str:
        """Chama o LLM especificado"""
        if provider == "openai" and self.openai_client:
            return await self._chamar_openai(messages)
        elif provider == "anthropic" and self.anthropic_client:
            return await self._chamar_anthropic(messages)
        elif provider == "gemini" and settings.GOOGLE_API_KEY:
            return await self._chamar_gemini(messages)
        else:
            # Fallback para o primeiro disponível
            if self.openai_client:
                return await self._chamar_openai(messages)
            elif self.anthropic_client:
                return await self._chamar_anthropic(messages)
            elif settings.GOOGLE_API_KEY:
                return await self._chamar_gemini(messages)
            else:
                raise Exception("Nenhum provedor de IA configurado")
    
    async def processar_contracheque(self, file_content: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        """Processa contracheque extraindo rubricas individuais"""
        try:
            # Extrair texto do arquivo
            if mime_type == 'application/pdf':
                texto_extraido = self._extrair_texto_pdf(file_content)
            else:
                raise Exception("Tipo de arquivo não suportado para contracheque")
            
            # Prompt especializado para contracheques
            system_message = """Você é um especialista em análise de contracheques do poder judiciário brasileiro.

INSTRUÇÕES CRÍTICAS PARA EXTRAÇÃO:
1. Identifique CADA linha do contracheque que representa uma rubrica
2. Para CADA rubrica, extraia APENAS:
   - DESCRIÇÃO: nome exato da rubrica
   - VALOR: SOMENTE das colunas "CRÉDITOS R$" ou "DÉBITOS R$"
3. REGRA DE CLASSIFICAÇÃO:
   - Se apenas a coluna "CRÉDITOS R$" estiver preenchida → é um CRÉDITO (receita)
   - Se apenas a coluna "DÉBITOS R$" estiver preenchida → é um DÉBITO (desconto)
4. Extraia informações do cabeçalho (empresa, funcionário, competência)
5. Retorne JSON válido sem markdown

ESTRUTURA DE RESPOSTA OBRIGATÓRIA:
{
  "rubricas_creditos": [
    {"descricao": "descrição exata da rubrica", "valor": 0.0}
  ],
  "rubricas_debitos": [
    {"descricao": "descrição exata da rubrica", "valor": 0.0}
  ],
  "empresa_pagadora": "nome da empresa",
  "funcionario": "nome do funcionário",
  "competencia_mes": 12,
  "competencia_ano": 2024,
  "data_pagamento": "2024-12-15",
  "valor_bruto_total": 0.0,
  "valor_liquido_total": 0.0
}"""

            user_message = f"Analise este contracheque ({filename}) e extraia TODAS as rubricas individuais. Texto: {texto_extraido[:3000]}"
            
            messages = [system_message, user_message]
            response = await self._chamar_llm(messages)
            
            # Processar resposta JSON
            try:
                response_clean = response.strip()
                if response_clean.startswith('```json'):
                    response_clean = response_clean.replace('```json', '').replace('```', '').strip()
                
                dados_json = json.loads(response_clean)
                
                # Validar e calcular totais
                rubricas_creditos = dados_json.get('rubricas_creditos', [])
                rubricas_debitos = dados_json.get('rubricas_debitos', [])
                
                total_creditos = sum(r['valor'] for r in rubricas_creditos)
                total_debitos = sum(r['valor'] for r in rubricas_debitos)
                
                dados_json['valor_bruto_total'] = round(total_creditos, 2)
                dados_json['valor_descontos_total'] = round(total_debitos, 2)
                dados_json['valor_liquido_total'] = round(total_creditos - total_debitos, 2)
                
                return dados_json
                
            except json.JSONDecodeError as json_error:
                logger.error(f"Erro ao parsear JSON: {json_error}")
                raise Exception(f"Erro ao processar resposta da IA: {json_error}")
                
        except Exception as e:
            logger.error(f"Erro no processamento do contracheque: {str(e)}")
            raise Exception(f"Erro no processamento: {str(e)}")
    
    async def processar_extrato_bancario(self, file_content: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        """Processa extrato bancário usando IA"""
        try:
            # Extrair texto do arquivo
            if mime_type == 'application/pdf':
                texto_extraido = self._extrair_texto_pdf(file_content)
            else:
                raise Exception("Tipo de arquivo não suportado para extrato bancário")
            
            # Prompt especializado para extratos bancários
            system_message = """Você é um especialista em análise de extratos bancários brasileiros.

INSTRUÇÕES CRÍTICAS PARA EXTRAÇÃO:
1. Identifique TODAS as transações do extrato bancário
2. Para CADA transação, extraia:
   - DATA: formato DD/MM/AAAA
   - DESCRIÇÃO: descrição completa da transação
   - VALOR: valor da transação (sempre positivo)
   - TIPO: "debito" (saída de dinheiro) ou "credito" (entrada de dinheiro)
3. Extraia informações do cabeçalho:
   - Nome do banco
   - Número da conta (últimos 4 dígitos)
   - Período do extrato (data início e fim)
   - Saldo inicial e final
4. Categorize automaticamente cada transação
5. Retorne JSON válido sem markdown

ESTRUTURA DE RESPOSTA OBRIGATÓRIA:
{
  "banco": "nome do banco",
  "conta": "número da conta (últimos 4 dígitos)",
  "periodo_inicio": "DD/MM/AAAA",
  "periodo_fim": "DD/MM/AAAA", 
  "saldo_inicial": 0.0,
  "saldo_final": 0.0,
  "transacoes": [
    {
      "data": "DD/MM/AAAA",
      "descricao": "descrição da transação",
      "valor": 0.0,
      "tipo": "debito ou credito",
      "categoria_sugerida": "categoria"
    }
  ],
  "total_debitos": 0.0,
  "total_creditos": 0.0,
  "total_transacoes": 0
}"""

            user_message = f"Analise este extrato bancário ({filename}) e extraia TODAS as transações. Texto: {texto_extraido[:4000]}"
            
            messages = [system_message, user_message]
            response = await self._chamar_llm(messages)
            
            # Processar resposta JSON
            try:
                response_clean = response.strip()
                if response_clean.startswith('```json'):
                    response_clean = response_clean.replace('```json', '').replace('```', '').strip()
                
                dados_json = json.loads(response_clean)
                
                # Validar e calcular totais
                transacoes = dados_json.get('transacoes', [])
                total_debitos = sum(t['valor'] for t in transacoes if t['tipo'] == 'debito')
                total_creditos = sum(t['valor'] for t in transacoes if t['tipo'] == 'credito')
                
                dados_json['total_debitos'] = round(total_debitos, 2)
                dados_json['total_creditos'] = round(total_creditos, 2)
                dados_json['total_transacoes'] = len(transacoes)
                
                return dados_json
                
            except json.JSONDecodeError as json_error:
                logger.error(f"Erro ao parsear JSON: {json_error}")
                raise Exception(f"Erro ao processar resposta da IA: {json_error}")
                
        except Exception as e:
            logger.error(f"Erro no processamento do extrato bancário: {str(e)}")
            raise Exception(f"Erro no processamento: {str(e)}")
    
    async def processar_extrato_cartao(self, file_content: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        """Processa extrato de cartão de crédito usando IA"""
        try:
            # Extrair texto do arquivo
            if mime_type == 'application/pdf':
                texto_extraido = self._extrair_texto_pdf(file_content)
            else:
                raise Exception("Tipo de arquivo não suportado para extrato de cartão")
            
            # Prompt especializado para extratos de cartão
            system_message = """Você é um especialista em análise de extratos de cartão de crédito brasileiros.

INSTRUÇÕES CRÍTICAS PARA EXTRAÇÃO:
1. Identifique TODAS as transações do cartão de crédito
2. Para CADA transação, extraia:
   - DATA: formato DD/MM/AAAA (data da compra)
   - DESCRIÇÃO: estabelecimento e descrição completa
   - VALOR: valor da transação
   - PARCELA: se é parcelado (ex: "2/12")
3. Extraia informações da fatura:
   - Bandeira do cartão (Visa, Mastercard, etc.)
   - Últimos 4 dígitos do cartão
   - Período da fatura
   - Valor total da fatura
   - Data de vencimento
4. Categorize automaticamente cada transação
5. Retorne JSON válido sem markdown

ESTRUTURA DE RESPOSTA OBRIGATÓRIA:
{
  "bandeira_cartao": "Visa/Mastercard/etc",
  "numero_final_cartao": "últimos 4 dígitos",
  "periodo_inicio": "DD/MM/AAAA",
  "periodo_fim": "DD/MM/AAAA",
  "valor_fatura": 0.0,
  "data_vencimento": "DD/MM/AAAA",
  "transacoes": [
    {
      "data": "DD/MM/AAAA",
      "descricao": "estabelecimento - descrição",
      "valor": 0.0,
      "categoria_sugerida": "categoria",
      "parcela": "1/1 ou 2/12 etc"
    }
  ],
  "total_gastos": 0.0,
  "total_transacoes": 0
}"""

            user_message = f"Analise este extrato de cartão de crédito ({filename}) e extraia TODAS as transações. Texto: {texto_extraido[:4000]}"
            
            messages = [system_message, user_message]
            response = await self._chamar_llm(messages)
            
            # Processar resposta JSON
            try:
                response_clean = response.strip()
                if response_clean.startswith('```json'):
                    response_clean = response_clean.replace('```json', '').replace('```', '').strip()
                
                dados_json = json.loads(response_clean)
                
                # Validar e calcular totais
                transacoes = dados_json.get('transacoes', [])
                total_gastos = sum(t['valor'] for t in transacoes)
                
                dados_json['total_gastos'] = round(total_gastos, 2)
                dados_json['total_transacoes'] = len(transacoes)
                
                return dados_json
                
            except json.JSONDecodeError as json_error:
                logger.error(f"Erro ao parsear JSON: {json_error}")
                raise Exception(f"Erro ao processar resposta da IA: {json_error}")
                
        except Exception as e:
            logger.error(f"Erro no processamento do extrato de cartão: {str(e)}")
            raise Exception(f"Erro no processamento: {str(e)}")

# Instância global do serviço
processamento_arquivos = ProcessamentoArquivos()
