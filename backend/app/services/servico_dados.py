import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

class ServicosDados:
    def __init__(self):
        self.data_file_path = settings.DATA_FILE_PATH
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Garante que o arquivo de dados existe"""
        if not os.path.exists(self.data_file_path):
            os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
            self._create_initial_data_file()
    
    def _create_initial_data_file(self):
        """Cria o arquivo de dados inicial"""
        initial_data = {
            "gastos": [],
            "receitas": [],
            "contas": [],
            "categorias": {
                "gastos": [
                    {"id": "cat-gasto-1", "nome": "Alimentação", "tipo": "gasto", "cor": "#FF6B6B", "icone": "utensils", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-2", "nome": "Transporte", "tipo": "gasto", "cor": "#4ECDC4", "icone": "car", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-3", "nome": "Saúde", "tipo": "gasto", "cor": "#45B7D1", "icone": "heart", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-4", "nome": "Educação", "tipo": "gasto", "cor": "#F7DC6F", "icone": "book", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-5", "nome": "Lazer", "tipo": "gasto", "cor": "#BB8FCE", "icone": "smile", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-6", "nome": "Casa", "tipo": "gasto", "cor": "#85C1E9", "icone": "home", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-7", "nome": "Impostos e taxas públicas", "tipo": "gasto", "cor": "#EC7063", "icone": "file-text", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-8", "nome": "Empréstimos", "tipo": "gasto", "cor": "#F1948A", "icone": "credit-card", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-9", "nome": "Pensão alimentícia", "tipo": "gasto", "cor": "#D7BDE2", "icone": "heart-handshake", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-10", "nome": "Previdência pública", "tipo": "gasto", "cor": "#A9DFBF", "icone": "shield", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-11", "nome": "Previdência privada", "tipo": "gasto", "cor": "#A2D9CE", "icone": "umbrella", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-12", "nome": "Associação", "tipo": "gasto", "cor": "#F9E79F", "icone": "users", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-13", "nome": "Abate teto", "tipo": "gasto", "cor": "#FADBD8", "icone": "trending-down", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-gasto-14", "nome": "Outros", "tipo": "gasto", "cor": "#95A5A6", "icone": "more-horizontal", "created_at": "2024-01-01T00:00:00Z"}
                ],
                "receitas": [
                    {"id": "cat-receita-1", "nome": "Salário", "tipo": "receita", "cor": "#27AE60", "icone": "briefcase", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-receita-2", "nome": "Aulas/Palestras", "tipo": "receita", "cor": "#3498DB", "icone": "graduation-cap", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-receita-3", "nome": "Investimentos", "tipo": "receita", "cor": "#E74C3C", "icone": "trending-up", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-receita-4", "nome": "Vendas", "tipo": "receita", "cor": "#9B59B6", "icone": "shopping-bag", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-receita-5", "nome": "Restituição de imposto de renda", "tipo": "receita", "cor": "#1ABC9C", "icone": "refund", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-receita-6", "nome": "Reembolsos", "tipo": "receita", "cor": "#F39C12", "icone": "rotate-ccw", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-receita-7", "nome": "Ações judiciais", "tipo": "receita", "cor": "#8E44AD", "icone": "scales", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-receita-8", "nome": "Adicionais", "tipo": "receita", "cor": "#2ECC71", "icone": "plus", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-receita-9", "nome": "Gratificação", "tipo": "receita", "cor": "#E67E22", "icone": "award", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-receita-10", "nome": "Verbas indenizatórias", "tipo": "receita", "cor": "#16A085", "icone": "shield-check", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-receita-11", "nome": "Resgates de investimentos", "tipo": "receita", "cor": "#C0392B", "icone": "piggy-bank", "created_at": "2024-01-01T00:00:00Z"},
                    {"id": "cat-receita-12", "nome": "Outros", "tipo": "receita", "cor": "#95A5A6", "icone": "more-horizontal", "created_at": "2024-01-01T00:00:00Z"}
                ]
            },
            "investimentos": [],
            "contracheques_processados": [],
            "extratos_bancarios_processados": [],
            "extratos_cartao_processados": [],
            "llm_configs": [],
            "metas": [],
            "gastos_recorrentes": [],
            "compras_parceladas": [],
            "backup_metadata": {
                "last_backup": None,
                "version": "1.0.0",
                "total_records": 0
            }
        }
        self.save_data(initial_data)
    
    def load_data(self) -> Dict[str, Any]:
        """Carrega os dados do arquivo JSON"""
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.warning(f"Arquivo de dados não encontrado: {self.data_file_path}")
            self._create_initial_data_file()
            return self.load_data()
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            raise Exception(f"Arquivo de dados corrompido: {e}")
    
    def save_data(self, data: Dict[str, Any]) -> None:
        """Salva os dados no arquivo JSON"""
        try:
            # Atualizar metadata de backup
            data["backup_metadata"]["last_backup"] = datetime.now().isoformat()
            data["backup_metadata"]["total_records"] = (
                len(data.get("gastos", [])) + 
                len(data.get("receitas", [])) + 
                len(data.get("contas", [])) + 
                len(data.get("investimentos", []))
            )
            
            with open(self.data_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            logger.error(f"Erro ao salvar dados: {e}")
            raise Exception(f"Erro ao salvar dados: {e}")
    
    # Métodos para gastos
    def get_gastos(self, filtros: Optional[Dict] = None) -> List[Dict]:
        """Obtém lista de gastos com filtros opcionais"""
        data = self.load_data()
        gastos = data.get("gastos", [])
        
        if filtros:
            # Implementar filtros aqui (por data, categoria, etc.)
            pass
        
        return gastos
    
    def create_gasto(self, gasto_data: Dict) -> Dict:
        """Cria um novo gasto"""
        data = self.load_data()
        gasto_data["created_at"] = datetime.now().isoformat()
        data["gastos"].append(gasto_data)
        self.save_data(data)
        return gasto_data
    
    def update_gasto(self, gasto_id: str, gasto_data: Dict) -> Optional[Dict]:
        """Atualiza um gasto existente"""
        data = self.load_data()
        gastos = data.get("gastos", [])
        
        for i, gasto in enumerate(gastos):
            if gasto.get("id") == gasto_id:
                gastos[i].update(gasto_data)
                self.save_data(data)
                return gastos[i]
        
        return None
    
    def delete_gasto(self, gasto_id: str) -> bool:
        """Remove um gasto"""
        data = self.load_data()
        gastos = data.get("gastos", [])
        
        for i, gasto in enumerate(gastos):
            if gasto.get("id") == gasto_id:
                del gastos[i]
                self.save_data(data)
                return True
        
        return False
    
    # Métodos para receitas
    def get_receitas(self, filtros: Optional[Dict] = None) -> List[Dict]:
        """Obtém lista de receitas com filtros opcionais"""
        data = self.load_data()
        receitas = data.get("receitas", [])
        
        if filtros:
            # Implementar filtros aqui
            pass
        
        return receitas
    
    def create_receita(self, receita_data: Dict) -> Dict:
        """Cria uma nova receita"""
        data = self.load_data()
        receita_data["created_at"] = datetime.now().isoformat()
        data["receitas"].append(receita_data)
        self.save_data(data)
        return receita_data
    
    def update_receita(self, receita_id: str, receita_data: Dict) -> Optional[Dict]:
        """Atualiza uma receita existente"""
        data = self.load_data()
        receitas = data.get("receitas", [])
        
        for i, receita in enumerate(receitas):
            if receita.get("id") == receita_id:
                receitas[i].update(receita_data)
                self.save_data(data)
                return receitas[i]
        
        return None
    
    def delete_receita(self, receita_id: str) -> bool:
        """Remove uma receita"""
        data = self.load_data()
        receitas = data.get("receitas", [])
        
        for i, receita in enumerate(receitas):
            if receita.get("id") == receita_id:
                del receitas[i]
                self.save_data(data)
                return True
        
        return False
    
    # Métodos para contas
    def get_contas(self) -> List[Dict]:
        """Obtém lista de contas"""
        data = self.load_data()
        return data.get("contas", [])
    
    def create_conta(self, conta_data: Dict) -> Dict:
        """Cria uma nova conta"""
        data = self.load_data()
        conta_data["created_at"] = datetime.now().isoformat()
        data["contas"].append(conta_data)
        self.save_data(data)
        return conta_data
    
    def update_conta(self, conta_id: str, conta_data: Dict) -> Optional[Dict]:
        """Atualiza uma conta existente"""
        data = self.load_data()
        contas = data.get("contas", [])
        
        for i, conta in enumerate(contas):
            if conta.get("id") == conta_id:
                contas[i].update(conta_data)
                self.save_data(data)
                return contas[i]
        
        return None
    
    def delete_conta(self, conta_id: str) -> bool:
        """Remove uma conta"""
        data = self.load_data()
        contas = data.get("contas", [])
        
        for i, conta in enumerate(contas):
            if conta.get("id") == conta_id:
                del contas[i]
                self.save_data(data)
                return True
        
        return False
    
    # Métodos para categorias
    def get_categorias(self) -> Dict[str, List[Dict]]:
        """Obtém todas as categorias"""
        data = self.load_data()
        return data.get("categorias", {"gastos": [], "receitas": []})
    
    # Métodos para investimentos
    def get_investimentos(self) -> List[Dict]:
        """Obtém lista de investimentos"""
        data = self.load_data()
        return data.get("investimentos", [])
    
    def create_investimento(self, investimento_data: Dict) -> Dict:
        """Cria um novo investimento"""
        data = self.load_data()
        investimento_data["created_at"] = datetime.now().isoformat()
        data["investimentos"].append(investimento_data)
        self.save_data(data)
        return investimento_data
    
    # Métodos para processamento de documentos
    def save_contracheque_processado(self, contracheque_data: Dict) -> Dict:
        """Salva um contracheque processado"""
        data = self.load_data()
        contracheque_data["created_at"] = datetime.now().isoformat()
        data["contracheques_processados"].append(contracheque_data)
        self.save_data(data)
        return contracheque_data
    
    def save_extrato_bancario_processado(self, extrato_data: Dict) -> Dict:
        """Salva um extrato bancário processado"""
        data = self.load_data()
        extrato_data["created_at"] = datetime.now().isoformat()
        data["extratos_bancarios_processados"].append(extrato_data)
        self.save_data(data)
        return extrato_data
    
    def save_extrato_cartao_processado(self, extrato_data: Dict) -> Dict:
        """Salva um extrato de cartão processado"""
        data = self.load_data()
        extrato_data["created_at"] = datetime.now().isoformat()
        data["extratos_cartao_processados"].append(extrato_data)
        self.save_data(data)
        return extrato_data
    
    # Métodos para configurações LLM
    def get_llm_configs(self) -> List[Dict]:
        """Obtém configurações de LLM"""
        data = self.load_data()
        return data.get("llm_configs", [])
    
    def save_llm_config(self, config_data: Dict) -> Dict:
        """Salva configuração de LLM"""
        data = self.load_data()
        config_data["created_at"] = datetime.now().isoformat()
        data["llm_configs"].append(config_data)
        self.save_data(data)
        return config_data

# Instância global do serviço
servico_dados = ServicosDados()
