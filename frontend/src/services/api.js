import axios from 'axios';

// Configuração base da API
const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 segundos
});

// Interceptador para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Erro na API:', error);
    
    if (error.response) {
      // Erro com resposta do servidor
      const message = error.response.data?.detail || 'Erro no servidor';
      throw new Error(message);
    } else if (error.request) {
      // Erro de rede
      throw new Error('Erro de conexão com o servidor');
    } else {
      // Outros erros
      throw new Error('Erro inesperado');
    }
  }
);

// === SERVIÇOS DE TRANSAÇÕES ===

export const transacoesService = {
  // Gastos
  listarGastos: (filtros = {}) => {
    const params = new URLSearchParams();
    Object.entries(filtros).forEach(([key, value]) => {
      if (value) params.append(key, value);
    });
    return api.get(`/transacoes/gastos?${params}`);
  },
  
  criarGasto: (gasto) => api.post('/transacoes/gastos', gasto),
  
  obterGasto: (id) => api.get(`/transacoes/gastos/${id}`),
  
  atualizarGasto: (id, gasto) => api.put(`/transacoes/gastos/${id}`, gasto),
  
  deletarGasto: (id) => api.delete(`/transacoes/gastos/${id}`),

  // Receitas
  listarReceitas: (filtros = {}) => {
    const params = new URLSearchParams();
    Object.entries(filtros).forEach(([key, value]) => {
      if (value) params.append(key, value);
    });
    return api.get(`/transacoes/receitas?${params}`);
  },
  
  criarReceita: (receita) => api.post('/transacoes/receitas', receita),
  
  obterReceita: (id) => api.get(`/transacoes/receitas/${id}`),
  
  atualizarReceita: (id, receita) => api.put(`/transacoes/receitas/${id}`, receita),
  
  deletarReceita: (id) => api.delete(`/transacoes/receitas/${id}`),

  // Categorias
  listarCategorias: () => api.get('/transacoes/categorias'),

  // Relatórios
  resumoMensal: (ano, mes) => api.get(`/transacoes/relatorios/resumo-mensal?ano=${ano}&mes=${mes}`),
};

// === SERVIÇOS DE CONTAS ===

export const contasService = {
  listar: () => api.get('/contas/contas'),
  
  criar: (conta) => api.post('/contas/contas', conta),
  
  obter: (id) => api.get(`/contas/contas/${id}`),
  
  atualizar: (id, conta) => api.put(`/contas/contas/${id}`, conta),
  
  deletar: (id) => api.delete(`/contas/contas/${id}`),
  
  calcularSaldo: (id) => api.get(`/contas/contas/${id}/saldo`),
  
  extrato: (id) => api.get(`/contas/contas/${id}/extrato`),
};

// === SERVIÇOS DE PROCESSAMENTO IA ===

export const processamentoService = {
  // Contracheques
  processarContracheque: (formData) => {
    return api.post('/processamento/contracheque/processar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000, // 2 minutos
    });
  },
  
  processarContrachequeDetalhado: (dados, arquivoNome) => {
    return api.post('/processamento/contracheque/processar-detalhado', dados, {
      params: { arquivo_nome: arquivoNome }
    });
  },
  
  listarContracheques: () => api.get('/processamento/contracheques/historico'),

  // Extratos Bancários
  processarExtratoBancario: (formData) => {
    return api.post('/processamento/extrato-bancario/processar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000,
    });
  },
  
  listarExtratosBancarios: () => api.get('/processamento/extratos-bancarios/historico'),

  // Extratos de Cartão
  processarExtratoCartao: (formData) => {
    return api.post('/processamento/extrato-cartao/processar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000,
    });
  },
  
  listarExtratosCartao: () => api.get('/processamento/extratos-cartao/historico'),
};

// === SERVIÇOS DE INVESTIMENTOS ===

export const investimentosService = {
  // Investimentos
  listar: (filtros = {}) => {
    const params = new URLSearchParams();
    Object.entries(filtros).forEach(([key, value]) => {
      if (value !== undefined && value !== null) params.append(key, value);
    });
    return api.get(`/investimentos/investimentos?${params}`);
  },
  
  criar: (investimento) => api.post('/investimentos/investimentos', investimento),
  
  obter: (id) => api.get(`/investimentos/investimentos/${id}`),
  
  atualizar: (id, investimento) => api.put(`/investimentos/investimentos/${id}`, investimento),
  
  deletar: (id) => api.delete(`/investimentos/investimentos/${id}`),
  
  resumo: () => api.get('/investimentos/investimentos/resumo'),

  // Metas
  listarMetas: (filtros = {}) => {
    const params = new URLSearchParams();
    Object.entries(filtros).forEach(([key, value]) => {
      if (value !== undefined && value !== null) params.append(key, value);
    });
    return api.get(`/investimentos/metas?${params}`);
  },
  
  criarMeta: (meta) => api.post('/investimentos/metas', meta),
  
  obterMeta: (id) => api.get(`/investimentos/metas/${id}`),
  
  atualizarMeta: (id, meta) => api.put(`/investimentos/metas/${id}`, meta),
  
  deletarMeta: (id) => api.delete(`/investimentos/metas/${id}`),
  
  contribuirMeta: (id, valor) => api.post(`/investimentos/metas/${id}/contribuir?valor=${valor}`),
  
  resumoMetas: () => api.get('/investimentos/metas/resumo'),
};

// === SERVIÇOS DE CONFIGURAÇÕES ===

export const configuracoesService = {
  // Configurações LLM
  listarConfigsLLM: () => api.get('/configuracoes/llm-configs'),
  
  criarConfigLLM: (config) => api.post('/configuracoes/llm-configs', config),
  
  deletarConfigLLM: (id) => api.delete(`/configuracoes/llm-configs/${id}`),
  
  alternarConfigLLM: (id) => api.put(`/configuracoes/llm-configs/${id}/toggle`),

  // Backup e Restore
  exportarDados: () => api.get('/configuracoes/backup/export'),
  
  importarDados: (dados) => api.post('/configuracoes/backup/import', dados),
  
  infoBackup: () => api.get('/configuracoes/backup/info'),

  // Sistema
  statusSistema: () => api.get('/configuracoes/sistema/status'),
  
  resetSistema: () => api.post('/configuracoes/sistema/reset'),
};

export default api;
