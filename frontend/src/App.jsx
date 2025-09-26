import React, { useState } from 'react'
import './App.css'
import LayoutSimple from './components/layout/LayoutSimple'
import DashboardSimple from './components/DashboardSimple'
import Login from './components/Login'
import Header from './components/Header'
import { useAuth } from './hooks/useAuth'

function App() {
  const [currentPage, setCurrentPage] = useState('/')
  const { isAuthenticated, isLoading, user, login, logout } = useAuth()

  // Mostrar loading enquanto verifica autenticação
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando...</p>
        </div>
      </div>
    )
  }

  // Mostrar tela de login se não estiver autenticado
  if (!isAuthenticated) {
    return <Login onLogin={login} />
  }

  const renderPage = () => {
    switch (currentPage) {
      case '/':
        return <DashboardSimple />
      case '/transacoes':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Transações</h2>
            <p className="text-gray-600">Funcionalidade em desenvolvimento...</p>
          </div>
        )
      case '/contas':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Contas</h2>
            <p className="text-gray-600">Funcionalidade em desenvolvimento...</p>
          </div>
        )
      case '/investimentos':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Investimentos</h2>
            <p className="text-gray-600">Funcionalidade em desenvolvimento...</p>
          </div>
        )
      case '/processamento':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Processamento IA</h2>
            <p className="text-gray-600">Funcionalidade em desenvolvimento...</p>
          </div>
        )
      case '/configuracoes':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Configurações</h2>
            <p className="text-gray-600">Funcionalidade em desenvolvimento...</p>
          </div>
        )
      default:
        return <DashboardSimple />
    }
  }

  // Mostrar aplicação principal se autenticado
  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} onLogout={logout} />
      <LayoutSimple currentPath={currentPage} onNavigate={setCurrentPage}>
        {renderPage()}
      </LayoutSimple>
    </div>
  )
}

export default App
