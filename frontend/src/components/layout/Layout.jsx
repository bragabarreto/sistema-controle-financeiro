import { useState } from 'react'
import { 
  Home, 
  TrendingDown, 
  TrendingUp, 
  CreditCard, 
  PiggyBank, 
  FileText, 
  Settings,
  Menu,
  X,
  DollarSign
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

const menuItems = [
  {
    title: 'Dashboard',
    icon: Home,
    path: '/',
    description: 'Visão geral das finanças'
  },
  {
    title: 'Gastos',
    icon: TrendingDown,
    path: '/gastos',
    description: 'Controle de despesas'
  },
  {
    title: 'Receitas',
    icon: TrendingUp,
    path: '/receitas',
    description: 'Controle de receitas'
  },
  {
    title: 'Contas',
    icon: CreditCard,
    path: '/contas',
    description: 'Contas bancárias e cartões'
  },
  {
    title: 'Investimentos',
    icon: PiggyBank,
    path: '/investimentos',
    description: 'Investimentos e metas'
  },
  {
    title: 'Processamento IA',
    icon: FileText,
    path: '/processamento',
    description: 'Processar documentos'
  },
  {
    title: 'Configurações',
    icon: Settings,
    path: '/configuracoes',
    description: 'Configurações do sistema'
  }
]

export default function Layout({ children, currentPath = '/', onNavigate }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={cn(
        "fixed inset-y-0 left-0 z-50 w-64 bg-card border-r border-border transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0",
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-border">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <DollarSign className="w-5 h-5 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-lg font-semibold text-foreground">FinanceControl</h1>
                <p className="text-xs text-muted-foreground">Sistema Financeiro</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              className="lg:hidden"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="w-4 h-4" />
            </Button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon
              const isActive = currentPath === item.path
              
              return (
                <button
                  key={item.path}
                  className={cn(
                    "w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-left transition-colors duration-200",
                    isActive 
                      ? "bg-primary text-primary-foreground shadow-sm" 
                      : "text-muted-foreground hover:text-foreground hover:bg-accent"
                  )}
                  onClick={() => {
                    if (onNavigate) {
                      onNavigate(item.path)
                    }
                    setSidebarOpen(false)
                  }}
                >
                  <Icon className="w-5 h-5 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium">{item.title}</div>
                    <div className="text-xs opacity-75 truncate">{item.description}</div>
                  </div>
                </button>
              )
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-border">
            <div className="text-xs text-muted-foreground text-center">
              <p>Sistema de Controle Financeiro</p>
              <p className="mt-1">v1.0.0</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:ml-64">
        {/* Top bar */}
        <header className="bg-card border-b border-border px-4 py-3 lg:px-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                className="lg:hidden"
                onClick={toggleSidebar}
              >
                <Menu className="w-5 h-5" />
              </Button>
              
              <div>
                <h2 className="text-xl font-semibold text-foreground">
                  {menuItems.find(item => item.path === currentPath)?.title || 'Dashboard'}
                </h2>
                <p className="text-sm text-muted-foreground">
                  {menuItems.find(item => item.path === currentPath)?.description || 'Visão geral das suas finanças'}
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <div className="hidden sm:block text-right">
                <p className="text-sm font-medium text-foreground">Sistema Online</p>
                <p className="text-xs text-muted-foreground">Dados sincronizados</p>
              </div>
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="p-4 lg:p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
