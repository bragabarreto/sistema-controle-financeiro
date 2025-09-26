import React, { useState, useRef } from 'react';
import dataService from '../services/dataService';
import googleDriveService from '../services/googleDriveService';

const ConfiguracoesAvancadas = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('info');
  const [googleCredentials, setGoogleCredentials] = useState({
    apiKey: '',
    clientId: ''
  });
  const [isGoogleConnected, setIsGoogleConnected] = useState(false);
  const fileInputRef = useRef(null);

  const showMessage = (text, type = 'info') => {
    setMessage(text);
    setMessageType(type);
    setTimeout(() => setMessage(''), 5000);
  };

  // Exportar dados para JSON
  const handleExportJSON = () => {
    try {
      dataService.exportToJSON();
      showMessage('Dados exportados com sucesso!', 'success');
    } catch (error) {
      showMessage('Erro ao exportar dados: ' + error.message, 'error');
    }
  };

  // Importar dados de JSON
  const handleImportJSON = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsLoading(true);
    try {
      await dataService.importFromJSON(file);
      showMessage('Dados importados com sucesso!', 'success');
      // Recarrega a página para atualizar os dados
      setTimeout(() => window.location.reload(), 1000);
    } catch (error) {
      showMessage('Erro ao importar dados: ' + error.message, 'error');
    } finally {
      setIsLoading(false);
      event.target.value = '';
    }
  };

  // Configurar credenciais do Google
  const handleGoogleCredentials = async () => {
    if (!googleCredentials.apiKey || !googleCredentials.clientId) {
      showMessage('Por favor, preencha API Key e Client ID', 'error');
      return;
    }

    setIsLoading(true);
    try {
      googleDriveService.setCredentials(googleCredentials.apiKey, googleCredentials.clientId);
      await googleDriveService.initialize();
      await googleDriveService.signIn();
      setIsGoogleConnected(true);
      showMessage('Google Drive conectado com sucesso!', 'success');
    } catch (error) {
      showMessage('Erro ao conectar Google Drive: ' + error.message, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  // Backup para Google Drive
  const handleBackupToGoogle = async () => {
    if (!isGoogleConnected) {
      showMessage('Conecte-se ao Google Drive primeiro', 'error');
      return;
    }

    setIsLoading(true);
    try {
      const data = dataService.getAllData();
      await googleDriveService.saveToGoogleDrive(data);
      showMessage('Backup salvo no Google Drive!', 'success');
    } catch (error) {
      showMessage('Erro ao fazer backup: ' + error.message, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  // Restaurar do Google Drive
  const handleRestoreFromGoogle = async () => {
    if (!isGoogleConnected) {
      showMessage('Conecte-se ao Google Drive primeiro', 'error');
      return;
    }

    setIsLoading(true);
    try {
      const data = await googleDriveService.loadFromGoogleDrive();
      dataService.saveToLocalStorage(data);
      showMessage('Dados restaurados do Google Drive!', 'success');
      setTimeout(() => window.location.reload(), 1000);
    } catch (error) {
      showMessage('Erro ao restaurar dados: ' + error.message, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  // Limpar todos os dados
  const handleClearData = () => {
    if (window.confirm('Tem certeza que deseja limpar todos os dados? Esta ação não pode ser desfeita.')) {
      dataService.clearAllData();
      showMessage('Todos os dados foram limpos!', 'success');
      setTimeout(() => window.location.reload(), 1000);
    }
  };

  // Desconectar Google Drive
  const handleDisconnectGoogle = async () => {
    try {
      await googleDriveService.signOut();
      setIsGoogleConnected(false);
      showMessage('Desconectado do Google Drive', 'info');
    } catch (error) {
      showMessage('Erro ao desconectar: ' + error.message, 'error');
    }
  };

  const statistics = dataService.getStatistics();

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Configurações Avançadas</h2>

      {/* Mensagem de status */}
      {message && (
        <div className={`mb-6 p-4 rounded-lg ${
          messageType === 'success' ? 'bg-green-50 text-green-700 border border-green-200' :
          messageType === 'error' ? 'bg-red-50 text-red-700 border border-red-200' :
          'bg-blue-50 text-blue-700 border border-blue-200'
        }`}>
          {message}
        </div>
      )}

      {/* Estatísticas */}
      <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
        <h3 className="text-lg font-semibold mb-4">📊 Estatísticas dos Dados</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              R$ {statistics.totalReceitas.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </div>
            <div className="text-sm text-gray-600">Total Receitas</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-red-600">
              R$ {statistics.totalGastos.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </div>
            <div className="text-sm text-gray-600">Total Gastos</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${statistics.saldo >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              R$ {statistics.saldo.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </div>
            <div className="text-sm text-gray-600">Saldo</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{statistics.totalTransacoes}</div>
            <div className="text-sm text-gray-600">Transações</div>
          </div>
        </div>
        <div className="mt-4 text-sm text-gray-500">
          Última atualização: {new Date(statistics.ultimaAtualizacao).toLocaleString('pt-BR')}
        </div>
      </div>

      {/* Backup/Restore Local */}
      <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
        <h3 className="text-lg font-semibold mb-4">💾 Backup Local (JSON)</h3>
        <div className="space-y-4">
          <div className="flex flex-wrap gap-3">
            <button
              onClick={handleExportJSON}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              📥 Exportar Dados
            </button>
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={isLoading}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
            >
              📤 Importar Dados
            </button>
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept=".json"
            onChange={handleImportJSON}
            className="hidden"
          />
          <p className="text-sm text-gray-600">
            Use o backup local para salvar seus dados em um arquivo JSON no seu computador.
          </p>
        </div>
      </div>

      {/* Google Drive Integration */}
      <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
        <h3 className="text-lg font-semibold mb-4">☁️ Sincronização Google Drive</h3>
        
        {!isGoogleConnected ? (
          <div className="space-y-4">
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h4 className="font-medium text-yellow-800 mb-2">🔧 Configuração Necessária</h4>
              <p className="text-sm text-yellow-700 mb-3">
                Para usar o Google Drive, você precisa configurar as credenciais da API:
              </p>
              <ol className="text-sm text-yellow-700 list-decimal list-inside space-y-1">
                <li>Acesse o <a href="https://console.developers.google.com" target="_blank" rel="noopener noreferrer" className="underline">Google Cloud Console</a></li>
                <li>Crie um projeto e ative a Google Drive API</li>
                <li>Crie credenciais (API Key e OAuth 2.0 Client ID)</li>
                <li>Insira as credenciais abaixo</li>
              </ol>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  API Key
                </label>
                <input
                  type="text"
                  value={googleCredentials.apiKey}
                  onChange={(e) => setGoogleCredentials(prev => ({ ...prev, apiKey: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Sua API Key do Google"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Client ID
                </label>
                <input
                  type="text"
                  value={googleCredentials.clientId}
                  onChange={(e) => setGoogleCredentials(prev => ({ ...prev, clientId: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Seu Client ID do Google"
                />
              </div>
            </div>
            
            <button
              onClick={handleGoogleCredentials}
              disabled={isLoading}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {isLoading ? '🔄 Conectando...' : '🔗 Conectar Google Drive'}
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <span className="text-green-700 font-medium">✅ Google Drive Conectado</span>
                <button
                  onClick={handleDisconnectGoogle}
                  className="text-sm text-red-600 hover:text-red-700"
                >
                  Desconectar
                </button>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-3">
              <button
                onClick={handleBackupToGoogle}
                disabled={isLoading}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
              >
                {isLoading ? '🔄 Salvando...' : '☁️ Backup para Drive'}
              </button>
              <button
                onClick={handleRestoreFromGoogle}
                disabled={isLoading}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                {isLoading ? '🔄 Restaurando...' : '📥 Restaurar do Drive'}
              </button>
            </div>
            
            <p className="text-sm text-gray-600">
              Seus dados serão salvos automaticamente na pasta "Financial Control" do seu Google Drive.
            </p>
          </div>
        )}
      </div>

      {/* Zona de Perigo */}
      <div className="bg-white rounded-lg shadow-sm border border-red-200 p-6">
        <h3 className="text-lg font-semibold mb-4 text-red-700">⚠️ Zona de Perigo</h3>
        <div className="space-y-4">
          <button
            onClick={handleClearData}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            🗑️ Limpar Todos os Dados
          </button>
          <p className="text-sm text-red-600">
            Esta ação irá remover permanentemente todos os seus dados financeiros. 
            Certifique-se de fazer um backup antes de prosseguir.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ConfiguracoesAvancadas;
