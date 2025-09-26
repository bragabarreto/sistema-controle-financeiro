# Guia de Deploy - Sistema de Controle Financeiro

## 🚀 Deploy Realizado

A aplicação foi desenvolvida e está disponível nos seguintes endereços:

### 🌐 Aplicação Online
- **URL Principal**: https://8000-i5j2uocx646rte9ugdhai-2e020f10.manusvm.computer
- **API Backend**: https://8000-i5j2uocx646rte9ugdhai-2e020f10.manusvm.computer/api/v1
- **Documentação API**: https://8000-i5j2uocx646rte9ugdhai-2e020f10.manusvm.computer/docs

### 📂 Repositório GitHub
- **URL**: https://github.com/bragabarreto/sistema-controle-financeiro
- **Branch Principal**: main
- **Código Completo**: Backend FastAPI + Frontend React

## 🏗️ Arquitetura Implementada

### Backend (FastAPI)
- **Framework**: FastAPI 0.115.6
- **Python**: 3.11
- **Banco de Dados**: JSON (schemas.json)
- **IA**: Suporte a OpenAI, Anthropic, Google Gemini
- **Documentação**: Swagger UI automática

### Frontend (React)
- **Framework**: React 18 + Vite
- **UI**: Tailwind CSS + shadcn/ui
- **Gráficos**: Recharts
- **Build**: Otimizado para produção

## 📊 Funcionalidades Implementadas

### ✅ Controle Financeiro Básico
- Dashboard com resumo financeiro
- Gestão de gastos e receitas
- Categorização automática
- Contas bancárias e cartões
- Relatórios visuais

### ✅ Processamento de IA
- Upload de contracheques (PDF/imagem)
- Extração automática de rubricas
- Processamento de extratos bancários
- Processamento de extratos de cartão
- Múltiplos provedores de IA

### ✅ Investimentos e Metas
- Carteira de investimentos
- Metas financeiras
- Acompanhamento de rentabilidade
- Sistema de contribuições

### ✅ Configurações Avançadas
- Gerenciamento de chaves API
- Backup e restore de dados
- Configurações de sistema
- Status e monitoramento

## 🔧 Como Usar

### 1. Acesso à Aplicação
1. Acesse: https://8000-i5j2uocx646rte9ugdhai-2e020f10.manusvm.computer
2. A interface carregará automaticamente
3. Navegue pelo menu lateral

### 2. Configuração Inicial
1. Vá em **Configurações** → **Configurações LLM**
2. Adicione suas chaves API:
   - OpenAI API Key
   - Anthropic API Key
   - Google API Key
3. Ative os provedores desejados

### 3. Processamento de Documentos
1. Acesse **Processamento IA**
2. Escolha o tipo de documento:
   - Contracheques
   - Extratos Bancários
   - Extratos de Cartão
3. Faça upload do arquivo (PDF/imagem)
4. Revise os dados extraídos
5. Importe as transações

### 4. Gestão Financeira
1. **Dashboard**: Visualize resumo geral
2. **Gastos**: Registre e categorize despesas
3. **Receitas**: Controle entradas financeiras
4. **Contas**: Gerencie contas bancárias
5. **Investimentos**: Acompanhe aplicações

## 🛠️ Deploy Local

### Pré-requisitos
```bash
# Python 3.11+
python3.11 --version

# Node.js 18+
node --version

# pnpm
npm install -g pnpm
```

### Backend
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
pnpm install
pnpm run build
# Os arquivos são copiados automaticamente para backend/app/static
```

### Execução
```bash
cd backend
source venv/bin/activate
python app.py
# Aplicação disponível em http://localhost:8000
```

## 📁 Estrutura de Arquivos

```
sistema-controle-financeiro/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── api/v1/            # Endpoints REST
│   │   ├── core/              # Configurações
│   │   ├── models/            # Modelos Pydantic
│   │   ├── services/          # Lógica de negócio
│   │   ├── data/              # Armazenamento JSON
│   │   └── static/            # Frontend buildado
│   ├── venv/                  # Ambiente virtual
│   ├── requirements.txt       # Dependências Python
│   └── app.py                 # Ponto de entrada
├── frontend/                  # Interface React
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── services/          # Cliente API
│   │   └── lib/               # Utilitários
│   ├── dist/                  # Build de produção
│   └── package.json           # Dependências Node
├── README.md                  # Documentação principal
└── DEPLOY.md                  # Este arquivo
```

## 🔒 Segurança

- **Dados Locais**: Armazenamento em JSON local
- **APIs Seguras**: Chaves não expostas no frontend
- **CORS**: Configurado adequadamente
- **Validação**: Entrada de dados sanitizada

## 📈 Próximos Passos

### Melhorias Sugeridas
1. **Integração Bancária**: Open Banking APIs
2. **App Mobile**: React Native
3. **Relatórios PDF**: Geração automática
4. **Notificações**: Alertas e lembretes
5. **Multi-usuário**: Sistema de autenticação

### Escalabilidade
1. **Banco de Dados**: Migração para PostgreSQL
2. **Cache**: Redis para performance
3. **Queue**: Celery para processamento assíncrono
4. **Monitoramento**: Logs e métricas

## 🆘 Suporte

- **Repositório**: https://github.com/bragabarreto/sistema-controle-financeiro
- **Issues**: Reporte bugs via GitHub Issues
- **Documentação API**: /docs na aplicação
- **Código Fonte**: Totalmente open source

---

**Sistema desenvolvido com foco na praticidade e segurança para controle financeiro pessoal.**
