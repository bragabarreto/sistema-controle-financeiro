import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  CreditCard,
  PieChart,
  Calendar,
  ArrowUpRight,
  ArrowDownRight,
  Plus
} from 'lucide-react'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart as RechartsPieChart,
  Cell
} from 'recharts'
import { formatarMoeda, formatarPercentual, obterCorCategoria } from '@/lib/utils'
import { transacoesService } from '@/services/api'

export default function Dashboard() {
  const [loading, setLoading] = useState(true)
  const [resumoMensal, setResumoMensal] = useState(null)
  const [gastos, setGastos] = useState([])
  const [receitas, setReceitas] = useState([])

  useEffect(() => {
    carregarDados()
  }, [])

  const carregarDados = async () => {
    try {
      setLoading(true)
      const hoje = new Date()
      const ano = hoje.getFullYear()
      const mes = hoje.getMonth() + 1

      // Carregar resumo mensal
      const resumoResponse = await transacoesService.resumoMensal(ano, mes)
      setResumoMensal(resumoResponse.data)

      // Carregar transações recentes
      const gastosResponse = await transacoesService.listarGastos()
      const receitasResponse = await transacoesService.listarReceitas()
      
      setGastos(gastosResponse.data.slice(0, 5)) // Últimos 5 gastos
      setReceitas(receitasResponse.data.slice(0, 5)) // Últimas 5 receitas

    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  // Preparar dados para gráficos
  const dadosGraficoBarras = resumoMensal ? [
    {
      nome: 'Receitas',
      valor: resumoMensal.total_receitas,
      cor: '#27AE60'
    },
    {
      nome: 'Gastos',
      valor: resumoMensal.total_gastos,
      cor: '#E74C3C'
    }
  ] : []

  const dadosGraficoPizza = resumoMensal ? 
    Object.entries(resumoMensal.gastos_por_categoria || {}).map(([categoria, valor]) => ({
      name: categoria,
      value: valor,
      color: obterCorCategoria(categoria)
    })) : []

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <div className="h-4 bg-muted rounded w-20"></div>
                <div className="h-4 w-4 bg-muted rounded"></div>
              </CardHeader>
              <CardContent>
                <div className="h-8 bg-muted rounded w-24 mb-2"></div>
                <div className="h-3 bg-muted rounded w-32"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
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
              {formatarMoeda(resumoMensal?.total_receitas || 0)}
            </div>
            <p className="text-xs text-muted-foreground">
              {resumoMensal?.periodo || 'Mês atual'}
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
              {formatarMoeda(resumoMensal?.total_gastos || 0)}
            </div>
            <p className="text-xs text-muted-foreground">
              {resumoMensal?.periodo || 'Mês atual'}
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Saldo
            </CardTitle>
            <DollarSign className={`h-4 w-4 ${(resumoMensal?.saldo || 0) >= 0 ? 'text-green-600' : 'text-red-600'}`} />
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${(resumoMensal?.saldo || 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {formatarMoeda(resumoMensal?.saldo || 0)}
            </div>
            <p className="text-xs text-muted-foreground flex items-center">
              {(resumoMensal?.saldo || 0) >= 0 ? (
                <ArrowUpRight className="h-3 w-3 mr-1" />
              ) : (
                <ArrowDownRight className="h-3 w-3 mr-1" />
              )}
              {(resumoMensal?.saldo || 0) >= 0 ? 'Positivo' : 'Negativo'}
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
              {resumoMensal?.quantidade_transacoes || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              Transações no mês
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Gráficos */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Gráfico de Barras - Receitas vs Gastos */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BarChart className="h-5 w-5" />
              <span>Receitas vs Gastos</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={dadosGraficoBarras}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="nome" />
                <YAxis tickFormatter={(value) => formatarMoeda(value)} />
                <Tooltip formatter={(value) => formatarMoeda(value)} />
                <Bar dataKey="valor" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Gráfico de Pizza - Gastos por Categoria */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <PieChart className="h-5 w-5" />
              <span>Gastos por Categoria</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <RechartsPieChart>
                <Pie
                  data={dadosGraficoPizza}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${formatarPercentual(percent * 100)}`}
                >
                  {dadosGraficoPizza.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => formatarMoeda(value)} />
              </RechartsPieChart>
            </ResponsiveContainer>
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
              {gastos.length > 0 ? gastos.map((gasto) => (
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
              )) : (
                <div className="text-center py-6 text-muted-foreground">
                  <TrendingDown className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>Nenhum gasto registrado</p>
                </div>
              )}
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
              {receitas.length > 0 ? receitas.map((receita) => (
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
              )) : (
                <div className="text-center py-6 text-muted-foreground">
                  <TrendingUp className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>Nenhuma receita registrada</p>
                </div>
              )}
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
