import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Upload, 
  FileText, 
  CreditCard, 
  Building, 
  Loader2,
  CheckCircle,
  AlertCircle,
  Eye,
  Download
} from 'lucide-react'
import { formatarMoeda, formatarData } from '@/lib/utils'
import { processamentoService } from '@/services/api'

export default function ProcessamentoDocumentos() {
  const [loading, setLoading] = useState(false)
  const [arquivo, setArquivo] = useState(null)
  const [resultadoProcessamento, setResultadoProcessamento] = useState(null)
  const [showDetalhamento, setShowDetalhamento] = useState(false)
  const [tipoProcessamento, setTipoProcessamento] = useState('contracheque')

  const handleFileUpload = async (event, tipo) => {
    const file = event.target.files[0]
    if (!file) return

    // Validar tipo de arquivo
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
    if (!allowedTypes.includes(file.type)) {
      alert('Tipo de arquivo não suportado. Use PDF, JPG ou PNG.')
      return
    }

    // Validar tamanho (10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('Arquivo muito grande. Tamanho máximo: 10MB')
      return
    }

    setArquivo(file)
    setResultadoProcessamento(null)
    setShowDetalhamento(false)
    setTipoProcessamento(tipo)

    const formData = new FormData()
    formData.append('arquivo', file)

    try {
      setLoading(true)
      
      let response
      switch (tipo) {
        case 'contracheque':
          response = await processamentoService.processarContracheque(formData)
          break
        case 'extrato-bancario':
          response = await processamentoService.processarExtratoBancario(formData)
          break
        case 'extrato-cartao':
          response = await processamentoService.processarExtratoCartao(formData)
          break
        default:
          throw new Error('Tipo de processamento não suportado')
      }
      
      setResultadoProcessamento(response.data)
      setShowDetalhamento(true)
      
    } catch (error) {
      console.error('Erro ao processar arquivo:', error)
      alert('Erro ao processar arquivo: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleProcessarDetalhado = async () => {
    if (!resultadoProcessamento || !arquivo) return

    try {
      setLoading(true)
      
      let response
      switch (tipoProcessamento) {
        case 'contracheque':
          response = await processamentoService.processarContrachequeDetalhado(
            resultadoProcessamento.dados_extraidos,
            arquivo.name
          )
          break
        // Adicionar outros tipos conforme necessário
        default:
          throw new Error('Processamento detalhado não implementado para este tipo')
      }

      alert(`${response.data.transacoes_criadas} transações foram importadas!`)
      setResultadoProcessamento(null)
      setShowDetalhamento(false)
      setArquivo(null)
      
      // Limpar input
      const fileInputs = document.querySelectorAll('input[type="file"]')
      fileInputs.forEach(input => input.value = '')
      
    } catch (error) {
      console.error('Erro ao processar detalhadamente:', error)
      alert('Erro ao importar transações: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const renderResultadoContracheque = (dados) => {
    if (!dados) return null

    return (
      <div className="space-y-4">
        {/* Informações Gerais */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-3 bg-blue-50 rounded-lg">
            <Building className="h-6 w-6 mx-auto mb-2 text-blue-600" />
            <p className="text-sm font-medium">{dados.empresa_pagadora || 'N/A'}</p>
            <p className="text-xs text-muted-foreground">Empresa</p>
          </div>
          <div className="text-center p-3 bg-green-50 rounded-lg">
            <FileText className="h-6 w-6 mx-auto mb-2 text-green-600" />
            <p className="text-sm font-medium">{formatarMoeda(dados.valor_bruto_total)}</p>
            <p className="text-xs text-muted-foreground">Valor Bruto</p>
          </div>
          <div className="text-center p-3 bg-red-50 rounded-lg">
            <CreditCard className="h-6 w-6 mx-auto mb-2 text-red-600" />
            <p className="text-sm font-medium">{formatarMoeda(dados.valor_descontos_total)}</p>
            <p className="text-xs text-muted-foreground">Descontos</p>
          </div>
          <div className="text-center p-3 bg-purple-50 rounded-lg">
            <CheckCircle className="h-6 w-6 mx-auto mb-2 text-purple-600" />
            <p className="text-sm font-medium">{formatarMoeda(dados.valor_liquido_total)}</p>
            <p className="text-xs text-muted-foreground">Valor Líquido</p>
          </div>
        </div>

        {/* Rubricas de Crédito */}
        {dados.rubricas_creditos && dados.rubricas_creditos.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="text-green-600">Créditos (Receitas)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {dados.rubricas_creditos.map((rubrica, index) => (
                  <div key={index} className="flex justify-between items-center p-2 bg-green-50 rounded">
                    <span className="text-sm">{rubrica.descricao}</span>
                    <span className="font-medium text-green-600">{formatarMoeda(rubrica.valor)}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Rubricas de Débito */}
        {dados.rubricas_debitos && dados.rubricas_debitos.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="text-red-600">Débitos (Descontos)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {dados.rubricas_debitos.map((rubrica, index) => (
                  <div key={index} className="flex justify-between items-center p-2 bg-red-50 rounded">
                    <span className="text-sm">{rubrica.descricao}</span>
                    <span className="font-medium text-red-600">{formatarMoeda(rubrica.valor)}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        <div className="flex justify-end space-x-2">
          <Button variant="outline" onClick={() => setShowDetalhamento(false)}>
            Cancelar
          </Button>
          <Button onClick={handleProcessarDetalhado} disabled={loading}>
            {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Importar Transações
          </Button>
        </div>
      </div>
    )
  }

  const renderUploadArea = (tipo, titulo, descricao, icone) => {
    const Icon = icone
    
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Icon className="h-5 w-5" />
            <span>{titulo}</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
              <input
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={(e) => handleFileUpload(e, tipo)}
                className="hidden"
                id={`file-${tipo}`}
                disabled={loading}
              />
              <label htmlFor={`file-${tipo}`} className="cursor-pointer">
                <Upload className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <p className="text-lg font-medium mb-2">Clique para fazer upload</p>
                <p className="text-sm text-muted-foreground mb-2">{descricao}</p>
                <p className="text-xs text-muted-foreground">
                  Formatos aceitos: PDF, JPG, PNG (máx. 10MB)
                </p>
              </label>
            </div>
            
            {loading && (
              <div className="flex items-center justify-center py-4">
                <Loader2 className="h-8 w-8 animate-spin mr-2" />
                <span>Processando documento...</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Processamento de Documentos</h1>
          <p className="text-muted-foreground">
            Use IA para extrair dados de contracheques, extratos bancários e de cartão
          </p>
        </div>
      </div>

      {showDetalhamento && resultadoProcessamento ? (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Dados Extraídos - {arquivo?.name}</span>
              <Button variant="outline" size="sm" onClick={() => setShowDetalhamento(false)}>
                <Eye className="h-4 w-4 mr-2" />
                Voltar
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {tipoProcessamento === 'contracheque' && 
              renderResultadoContracheque(resultadoProcessamento.dados_extraidos)}
          </CardContent>
        </Card>
      ) : (
        <Tabs defaultValue="contracheque" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="contracheque">Contracheques</TabsTrigger>
            <TabsTrigger value="extrato-bancario">Extratos Bancários</TabsTrigger>
            <TabsTrigger value="extrato-cartao">Extratos de Cartão</TabsTrigger>
          </TabsList>

          <TabsContent value="contracheque" className="space-y-4">
            {renderUploadArea(
              'contracheque',
              'Processar Contracheque',
              'Extraia automaticamente rubricas de créditos e débitos',
              FileText
            )}
          </TabsContent>

          <TabsContent value="extrato-bancario" className="space-y-4">
            {renderUploadArea(
              'extrato-bancario',
              'Processar Extrato Bancário',
              'Extraia transações de débito e crédito automaticamente',
              Building
            )}
          </TabsContent>

          <TabsContent value="extrato-cartao" className="space-y-4">
            {renderUploadArea(
              'extrato-cartao',
              'Processar Extrato de Cartão',
              'Extraia compras e parcelamentos automaticamente',
              CreditCard
            )}
          </TabsContent>
        </Tabs>
      )}

      {/* Informações sobre IA */}
      <Card className="bg-blue-50 border-blue-200">
        <CardContent className="pt-6">
          <div className="flex items-start space-x-3">
            <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5" />
            <div>
              <h3 className="font-medium text-blue-900">Como funciona o processamento</h3>
              <p className="text-sm text-blue-700 mt-1">
                Utilizamos inteligência artificial avançada para extrair dados dos seus documentos financeiros. 
                O sistema identifica automaticamente rubricas, valores e categorias, facilitando a importação 
                para seu controle financeiro.
              </p>
              <ul className="text-sm text-blue-700 mt-2 space-y-1">
                <li>• Processamento seguro e local dos documentos</li>
                <li>• Categorização automática baseada em IA</li>
                <li>• Validação e correção de dados extraídos</li>
                <li>• Suporte a múltiplos formatos (PDF, imagens)</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
