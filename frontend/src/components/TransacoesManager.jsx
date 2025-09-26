import React, { useState, useEffect } from 'react';
import dataService from '../services/dataService';

const TransacoesManager = () => {
  const [transacoes, setTransacoes] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingTransaction, setEditingTransaction] = useState(null);
  const [formData, setFormData] = useState({
    tipo: 'gasto',
    categoria: '',
    descricao: '',
    valor: '',
    data: new Date().toISOString().split('T')[0],
    conta: ''
  });

  const categorias = {
    gasto: ['Alimentação', 'Transporte', 'Moradia', 'Saúde', 'Educação', 'Lazer', 'Compras', 'Outros'],
    receita: ['Salário', 'Freelance', 'Investimentos', 'Vendas', 'Outros']
  };

  useEffect(() => {
    loadTransacoes();
  }, []);

  const loadTransacoes = () => {
    const data = dataService.getAllData();
    setTransacoes(data.transacoes || []);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const transacao = {
      ...formData,
      valor: parseFloat(formData.valor)
    };

    if (editingTransaction) {
      // Atualizar transação existente
      const data = dataService.getAllData();
      const index = data.transacoes.findIndex(t => t.id === editingTransaction.id);
      if (index !== -1) {
        data.transacoes[index] = { ...editingTransaction, ...transacao };
        dataService.saveToLocalStorage(data);
      }
      setEditingTransaction(null);
    } else {
      // Adicionar nova transação
      dataService.addTransacao(transacao);
    }

    // Reset form
    setFormData({
      tipo: 'gasto',
      categoria: '',
      descricao: '',
      valor: '',
      data: new Date().toISOString().split('T')[0],
      conta: ''
    });
    setShowForm(false);
    loadTransacoes();
  };

  const handleEdit = (transacao) => {
    setEditingTransaction(transacao);
    setFormData({
      tipo: transacao.tipo,
      categoria: transacao.categoria,
      descricao: transacao.descricao,
      valor: transacao.valor.toString(),
      data: transacao.data,
      conta: transacao.conta || ''
    });
    setShowForm(true);
  };

  const handleDelete = (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta transação?')) {
      dataService.removeTransacao(id);
      loadTransacoes();
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatDate = (dateString) => {
    return new Date(dateString + 'T00:00:00').toLocaleDateString('pt-BR');
  };

  const totalReceitas = transacoes
    .filter(t => t.tipo === 'receita')
    .reduce((sum, t) => sum + t.valor, 0);

  const totalGastos = transacoes
    .filter(t => t.tipo === 'gasto')
    .reduce((sum, t) => sum + t.valor, 0);

  const saldo = totalReceitas - totalGastos;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Transações</h2>
        <button
          onClick={() => setShowForm(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          + Nova Transação
        </button>
      </div>

      {/* Resumo */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <h3 className="text-sm font-medium text-green-700">Receitas</h3>
          <p className="text-2xl font-bold text-green-600">{formatCurrency(totalReceitas)}</p>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h3 className="text-sm font-medium text-red-700">Gastos</h3>
          <p className="text-2xl font-bold text-red-600">{formatCurrency(totalGastos)}</p>
        </div>
        <div className={`border rounded-lg p-4 ${saldo >= 0 ? 'bg-blue-50 border-blue-200' : 'bg-red-50 border-red-200'}`}>
          <h3 className={`text-sm font-medium ${saldo >= 0 ? 'text-blue-700' : 'text-red-700'}`}>Saldo</h3>
          <p className={`text-2xl font-bold ${saldo >= 0 ? 'text-blue-600' : 'text-red-600'}`}>
            {formatCurrency(saldo)}
          </p>
        </div>
      </div>

      {/* Formulário */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h3 className="text-lg font-semibold mb-4">
              {editingTransaction ? 'Editar Transação' : 'Nova Transação'}
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Tipo</label>
                <select
                  value={formData.tipo}
                  onChange={(e) => setFormData(prev => ({ ...prev, tipo: e.target.value, categoria: '' }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                >
                  <option value="gasto">Gasto</option>
                  <option value="receita">Receita</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Categoria</label>
                <select
                  value={formData.categoria}
                  onChange={(e) => setFormData(prev => ({ ...prev, categoria: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                >
                  <option value="">Selecione uma categoria</option>
                  {categorias[formData.tipo].map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Descrição</label>
                <input
                  type="text"
                  value={formData.descricao}
                  onChange={(e) => setFormData(prev => ({ ...prev, descricao: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Valor</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.valor}
                  onChange={(e) => setFormData(prev => ({ ...prev, valor: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Data</label>
                <input
                  type="date"
                  value={formData.data}
                  onChange={(e) => setFormData(prev => ({ ...prev, data: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  {editingTransaction ? 'Atualizar' : 'Salvar'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingTransaction(null);
                    setFormData({
                      tipo: 'gasto',
                      categoria: '',
                      descricao: '',
                      valor: '',
                      data: new Date().toISOString().split('T')[0],
                      conta: ''
                    });
                  }}
                  className="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Lista de Transações */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="p-4 border-b">
          <h3 className="font-semibold">Histórico de Transações</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">Data</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">Tipo</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">Categoria</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">Descrição</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-gray-700">Valor</th>
                <th className="px-4 py-3 text-center text-sm font-medium text-gray-700">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {transacoes.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-4 py-8 text-center text-gray-500">
                    Nenhuma transação encontrada. Clique em "Nova Transação" para começar.
                  </td>
                </tr>
              ) : (
                transacoes
                  .sort((a, b) => new Date(b.data) - new Date(a.data))
                  .map((transacao) => (
                    <tr key={transacao.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm">{formatDate(transacao.data)}</td>
                      <td className="px-4 py-3">
                        <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                          transacao.tipo === 'receita' 
                            ? 'bg-green-100 text-green-700' 
                            : 'bg-red-100 text-red-700'
                        }`}>
                          {transacao.tipo === 'receita' ? '↗️ Receita' : '↙️ Gasto'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm">{transacao.categoria}</td>
                      <td className="px-4 py-3 text-sm">{transacao.descricao}</td>
                      <td className={`px-4 py-3 text-sm text-right font-medium ${
                        transacao.tipo === 'receita' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {formatCurrency(transacao.valor)}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <div className="flex justify-center gap-2">
                          <button
                            onClick={() => handleEdit(transacao)}
                            className="text-blue-600 hover:text-blue-700 text-sm"
                          >
                            ✏️ Editar
                          </button>
                          <button
                            onClick={() => handleDelete(transacao.id)}
                            className="text-red-600 hover:text-red-700 text-sm"
                          >
                            🗑️ Excluir
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default TransacoesManager;
