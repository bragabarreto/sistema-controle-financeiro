import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  CreditCard,
  Plus,
  FileText,
  PieChart,
  Calendar
} from 'lucide-react'

export default function DashboardSimple() {
  const [loading, setLoading] = useState(false)

  // Dados mockados para demonstração
  const resumoMensal = {
    total_receitas: 5000,
    total_gastos: 3500,
    saldo: 1500,
    quantidade_transacoes: 25,
    periodo: "Setembro 2025"
  }

  const gastosRecentes = [
    { id: 1, descricao: "Supermercado", categoria: "Alimentação", valor: 250.00, data: "25/09/2025" },
    { id: 2, descricao: "Combustível", categoria: "Transporte", valor: 120.00, data: "24/09/2025" },
    { id: 3, descricao: "Farmácia", categoria: "Saúde", valor: 85.50, data: "23/09/2025" }
  ]

  const receitasRecentes = [
    { id: 1, descricao: "Salário", categoria: "Salário", valor: 5000.00, data: "01/09/2025" },
    { id: 2, descricao: "Freelance", categoria: "Aulas/Palestras", valor: 800.00, data: "15/09/2025" }
  ]

  const formatarMoeda = (valor) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(valor)
  }

  return (
    <div className="space-y-6">
      {/* Cards de Resumo */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Total Receitas
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {formatarMoeda(resumoMensal.total_receitas)}
            </div>
            <p className="text-xs text-muted-foreground">
              {resumoMensal.periodo}
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Total Gastos
            </CardTitle>
            <TrendingDown className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              {formatarMoeda(resumoMensal.total_gastos)}
            </div>
            <p className="text-xs text-muted-foreground">
              {resumoMensal.periodo}
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Saldo
            </CardTitle>
            <DollarSign className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {formatarMoeda(resumoMensal.saldo)}
            </div>
            <p className="text-xs text-muted-foreground">
              Positivo
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Transações
            </CardTitle>
            <CreditCard className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">
              {resumoMensal.quantidade_transacoes}
            </div>
            <p className="text-xs text-muted-foreground">
              Transações no mês
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Gráficos Placeholder */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5" />
              <span>Receitas vs Gastos</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-center justify-center bg-muted rounded-lg">
              <div className="text-center">
                <PieChart className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-muted-foreground">Gráfico será exibido aqui</p>
                <p className="text-sm text-muted-foreground">Receitas: {formatarMoeda(resumoMensal.total_receitas)}</p>
                <p className="text-sm text-muted-foreground">Gastos: {formatarMoeda(resumoMensal.total_gastos)}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <PieChart className="h-5 w-5" />
              <span>Gastos por Categoria</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-center justify-center bg-muted rounded-lg">
              <div className="text-center">
                <PieChart className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-muted-foreground">Gráfico de categorias</p>
                <div className="mt-4 space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Alimentação</span>
                    <span className="text-red-600">{formatarMoeda(250)}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Transporte</span>
                    <span className="text-red-600">{formatarMoeda(120)}</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Transações Recentes */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Gastos Recentes */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="flex items-center space-x-2">
              <TrendingDown className="h-5 w-5 text-red-600" />
              <span>Gastos Recentes</span>
            </CardTitle>
            <Button variant="outline" size="sm">
              <Plus className="h-4 w-4 mr-2" />
              Novo Gasto
            </Button>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {gastosRecentes.map((gasto) => (
                <div key={gasto.id} className="flex items-center justify-between p-3 rounded-lg border">
                  <div className="flex-1">
                    <p className="font-medium text-sm">{gasto.descricao}</p>
                    <p className="text-xs text-muted-foreground">{gasto.categoria}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-red-600">{formatarMoeda(gasto.valor)}</p>
                    <p className="text-xs text-muted-foreground">{gasto.data}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Receitas Recentes */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5 text-green-600" />
              <span>Receitas Recentes</span>
            </CardTitle>
            <Button variant="outline" size="sm">
              <Plus className="h-4 w-4 mr-2" />
              Nova Receita
            </Button>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {receitasRecentes.map((receita) => (
                <div key={receita.id} className="flex items-center justify-between p-3 rounded-lg border">
                  <div className="flex-1">
                    <p className="font-medium text-sm">{receita.descricao}</p>
                    <p className="text-xs text-muted-foreground">{receita.categoria}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-green-600">{formatarMoeda(receita.valor)}</p>
                    <p className="text-xs text-muted-foreground">{receita.data}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Ações Rápidas */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Calendar className="h-5 w-5" />
            <span>Ações Rápidas</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <Button className="h-20 flex flex-col space-y-2" variant="outline">
              <FileText className="h-6 w-6" />
              <span>Processar Contracheque</span>
            </Button>
            <Button className="h-20 flex flex-col space-y-2" variant="outline">
              <CreditCard className="h-6 w-6" />
              <span>Processar Extrato</span>
            </Button>
            <Button className="h-20 flex flex-col space-y-2" variant="outline">
              <PieChart className="h-6 w-6" />
              <span>Ver Relatórios</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
