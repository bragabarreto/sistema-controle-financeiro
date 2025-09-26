import React, { useState } from 'react';

const menuItems = [
  {
    title: 'Dashboard',
    path: '/',
    description: 'Visão geral das finanças',
    icon: '🏠'
  },
  {
    title: 'Gastos',
    path: '/gastos',
    description: 'Controle de despesas',
    icon: '📉'
  },
  {
    title: 'Receitas',
    path: '/receitas',
    description: 'Controle de receitas',
    icon: '📈'
  },
  {
    title: 'Contas',
    path: '/contas',
    description: 'Contas bancárias e cartões',
    icon: '💳'
  },
  {
    title: 'Investimentos',
    path: '/investimentos',
    description: 'Investimentos e metas',
    icon: '🐷'
  },
  {
    title: 'Processamento IA',
    path: '/processamento',
    description: 'Processar documentos',
    icon: '🤖'
  },
  {
    title: 'Configurações',
    path: '/configuracoes',
    description: 'Configurações do sistema',
    icon: '⚙️'
  }
];

export default function LayoutSimple({ children, currentPath = '/', onNavigate }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleNavigation = (path) => {
    console.log('Navegando para:', path);
    if (onNavigate) {
      onNavigate(path);
    }
    setSidebarOpen(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 ${
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      }`}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white text-sm">💰</span>
              </div>
              <div>
                <h1 className="text-lg font-semibold text-gray-900">FinanceControl</h1>
                <p className="text-xs text-gray-500">Sistema Financeiro</p>
              </div>
            </div>
            <button
              className="lg:hidden p-1 rounded-md hover:bg-gray-100"
              onClick={() => setSidebarOpen(false)}
            >
              <span className="text-gray-500">✕</span>
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2">
            {menuItems.map((item) => {
              const isActive = currentPath === item.path;
              
              return (
                <button
                  key={item.path}
                  className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-left transition-colors duration-200 ${
                    isActive 
                      ? "bg-blue-600 text-white shadow-sm" 
                      : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                  }`}
                  onClick={() => handleNavigation(item.path)}
                >
                  <span className="text-lg flex-shrink-0">{item.icon}</span>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium">{item.title}</div>
                    <div className="text-xs opacity-75 truncate">{item.description}</div>
                  </div>
                </button>
              );
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-gray-200">
            <div className="text-xs text-gray-500 text-center">
              <p>Sistema de Controle Financeiro</p>
              <p className="mt-1">v1.0.0</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 lg:ml-0">
        {/* Top bar */}
        <div className="bg-white border-b border-gray-200 lg:hidden">
          <div className="flex items-center justify-between p-4">
            <button
              className="p-2 rounded-md hover:bg-gray-100"
              onClick={() => setSidebarOpen(true)}
            >
              <span className="text-gray-600">☰</span>
            </button>
            <h1 className="text-lg font-semibold text-gray-900">Sistema Financeiro</h1>
            <div className="w-8"></div>
          </div>
        </div>

        {/* Page content */}
        <main className="flex-1">
          {children}
        </main>
      </div>
    </div>
  );
}
