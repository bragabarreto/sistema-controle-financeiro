// Serviço de persistência de dados
class DataService {
  constructor() {
    this.storageKey = 'financial-control-data';
    this.initializeData();
  }

  // Inicializa dados padrão se não existirem
  initializeData() {
    const existingData = this.loadFromLocalStorage();
    if (!existingData) {
      const defaultData = {
        version: '1.0.0',
        lastUpdated: new Date().toISOString(),
        user: 'bragabarreto',
        transacoes: [],
        contas: [
          {
            id: 1,
            nome: 'Conta Corrente',
            tipo: 'corrente',
            saldo: 5000.00,
            banco: 'Banco do Brasil'
          },
          {
            id: 2,
            nome: 'Cartão de Crédito',
            tipo: 'credito',
            limite: 3000.00,
            usado: 800.00,
            banco: 'Nubank'
          }
        ],
        investimentos: [],
        metas: [],
        configuracoes: {
          moeda: 'BRL',
          tema: 'light',
          notificacoes: true
        }
      };
      this.saveToLocalStorage(defaultData);
      return defaultData;
    }
    return existingData;
  }

  // Carrega dados do localStorage
  loadFromLocalStorage() {
    try {
      const data = localStorage.getItem(this.storageKey);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Erro ao carregar dados do localStorage:', error);
      return null;
    }
  }

  // Salva dados no localStorage
  saveToLocalStorage(data) {
    try {
      data.lastUpdated = new Date().toISOString();
      localStorage.setItem(this.storageKey, JSON.stringify(data, null, 2));
      return true;
    } catch (error) {
      console.error('Erro ao salvar dados no localStorage:', error);
      return false;
    }
  }

  // Obtém todos os dados
  getAllData() {
    return this.loadFromLocalStorage() || this.initializeData();
  }

  // Atualiza dados
  updateData(newData) {
    const currentData = this.getAllData();
    const updatedData = { ...currentData, ...newData };
    return this.saveToLocalStorage(updatedData);
  }

  // Adiciona transação
  addTransacao(transacao) {
    const data = this.getAllData();
    const newTransacao = {
      id: Date.now(),
      ...transacao,
      data: transacao.data || new Date().toISOString().split('T')[0],
      criado_em: new Date().toISOString()
    };
    data.transacoes.push(newTransacao);
    this.saveToLocalStorage(data);
    return newTransacao;
  }

  // Remove transação
  removeTransacao(id) {
    const data = this.getAllData();
    data.transacoes = data.transacoes.filter(t => t.id !== id);
    return this.saveToLocalStorage(data);
  }

  // Exporta dados para JSON
  exportToJSON() {
    const data = this.getAllData();
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json'
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `financial-data-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  // Importa dados de JSON
  async importFromJSON(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          if (this.validateDataStructure(data)) {
            this.saveToLocalStorage(data);
            resolve(data);
          } else {
            reject(new Error('Estrutura de dados inválida'));
          }
        } catch (error) {
          reject(new Error('Arquivo JSON inválido'));
        }
      };
      reader.onerror = () => reject(new Error('Erro ao ler arquivo'));
      reader.readAsText(file);
    });
  }

  // Valida estrutura dos dados
  validateDataStructure(data) {
    const requiredFields = ['version', 'user', 'transacoes', 'contas'];
    return requiredFields.every(field => data.hasOwnProperty(field));
  }

  // Limpa todos os dados
  clearAllData() {
    localStorage.removeItem(this.storageKey);
    return this.initializeData();
  }

  // Obtém estatísticas
  getStatistics() {
    const data = this.getAllData();
    const transacoes = data.transacoes || [];
    
    const receitas = transacoes
      .filter(t => t.tipo === 'receita')
      .reduce((sum, t) => sum + (t.valor || 0), 0);
    
    const gastos = transacoes
      .filter(t => t.tipo === 'gasto')
      .reduce((sum, t) => sum + (t.valor || 0), 0);
    
    return {
      totalReceitas: receitas,
      totalGastos: gastos,
      saldo: receitas - gastos,
      totalTransacoes: transacoes.length,
      ultimaAtualizacao: data.lastUpdated
    };
  }
}

// Instância singleton
const dataService = new DataService();
export default dataService;
