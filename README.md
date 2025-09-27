# Sistema de Controle Financeiro

Um sistema completo de gestão financeira pessoal com processamento inteligente de documentos via IA.

## 🌐 **APLICAÇÃO ONLINE**

### 🚀 **Site Publicado**
- **URL Principal**: https://bragabarreto.github.io/sistema-controle-financeiro/ *(GitHub Pages)*
- **URL Alternativa**: https://sistema-controle-financeiro.manus.im *(Manus Deploy)*
- **Repositório GitHub**: https://github.com/bragabarreto/sistema-controle-financeiro
- **Status**: ✅ Deploy permanente realizado com sucesso

### 📋 **Como Ativar o Site (GitHub Pages)**
1. Acesse: https://github.com/bragabarreto/sistema-controle-financeiro/settings/pages
2. Em "Source", selecione "Deploy from a branch"
3. Escolha o branch "gh-pages" e pasta "/ (root)"
4. Clique em "Save"
5. O site estará disponível em: https://bragabarreto.github.io/sistema-controle-financeiro/

### 🔐 **Acesso Seguro**
A aplicação possui **sistema de autenticação** para proteger informações financeiras:

**Credenciais de Acesso:**
- **Usuário**: `bragabarreto`
- **Senha**: `Mimilulu1719#`

### 📱 **Funcionalidades Completas**
A aplicação está **100% funcional** e inclui:
- **Sistema de Login**: Autenticação segura com persistência de sessão
- **Interface moderna**: Design responsivo com Tailwind CSS
- **Dashboard interativo**: Gráficos dinâmicos e métricas em tempo real
- **Processamento IA**: Análise de documentos via OpenAI, Anthropic e Google Gemini
- **Categorização personalizada**: Categorias divididas em Despesas, Gastos e Investimentos, totalmente personalizáveis
- **Contas bancárias**: Gerenciamento de múltiplas contas e cartões
- **Investimentos**: Controle de aplicações e metas financeiras
- **Parcelamentos**: Sistema completo de controle de parcelas
- **Gastos recorrentes**: Automação de lançamentos periódicos
- **Backup/restore**: Exportação e importação de dados
- **Relatórios avançados**: Gráficos e análises detalhadas

## 🚀 Funcionalidades

### 💰 Controle Financeiro
- **Gestão de Gastos**: Registro e categorização de despesas
- **Controle de Receitas**: Acompanhamento de entradas financeiras
- **Contas Bancárias**: Gerenciamento de múltiplas contas e cartões
- **Relatórios**: Análises detalhadas e visualizações gráficas

### 🤖 Processamento Inteligente
- **Contracheques**: Extração automática de rubricas via IA
- **Extratos Bancários**: Processamento de transações bancárias
- **Extratos de Cartão**: Análise de faturas e parcelamentos
- **SMS de Cartão**: Processamento de mensagens SMS de transações
- **OCR para PIX**: Reconhecimento de comprovantes de transferências
- **Documentos de Receitas**: Upload e processamento de comprovantes
- **Múltiplos Provedores**: Suporte a OpenAI, Anthropic e Google Gemini

### 📊 Investimentos e Metas
- **Carteira de Investimentos**: Controle de aplicações financeiras
- **Metas Financeiras**: Sistema de objetivos e acompanhamento
- **Rentabilidade**: Cálculos automáticos de performance

## 🏗️ Arquitetura

### Backend (FastAPI)
- **API RESTful** com documentação automática
- **Processamento de IA** para documentos financeiros
- **Armazenamento JSON** para simplicidade e portabilidade
- **Validação de dados** com Pydantic

### Frontend (React)
- **Interface moderna** com Tailwind CSS e shadcn/ui
- **Dashboard interativo** com gráficos e métricas
- **Upload de documentos** com feedback em tempo real
- **Design responsivo** para desktop e mobile

## 🛠️ Tecnologias

### Backend
- **FastAPI** - Framework web moderno e rápido
- **Python 3.11** - Linguagem de programação
- **Pydantic** - Validação de dados
- **OpenAI/Anthropic/Gemini** - APIs de IA

### Frontend
- **React 18** - Biblioteca de interface
- **Vite** - Build tool e dev server
- **Tailwind CSS** - Framework de estilos
- **shadcn/ui** - Componentes de interface

## 📦 Instalação e Execução

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd frontend
pnpm install
pnpm run dev --host
```

## 🔧 Configuração

### Configuração de IA
As chaves de API podem ser configuradas diretamente na interface:
1. Acesse **Configurações** → **Configurações LLM**
2. Adicione suas chaves API dos provedores desejados
3. Ative/desative provedores conforme necessário

## 📊 Uso

### 1. Dashboard
- Visualize resumo financeiro mensal
- Acompanhe receitas vs gastos
- Veja transações recentes

### 2. Processamento de Documentos
- Faça upload de contracheques (PDF/imagem)
- Processe extratos bancários automaticamente
- Revise e importe transações extraídas

### 3. Gestão de Transações
- Registre gastos e receitas manualmente
- Categorize automaticamente
- Edite e exclua transações

## 📁 Estrutura do Projeto

```
financial-control-system/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints da API
│   │   ├── core/           # Configurações
│   │   ├── models/         # Modelos Pydantic
│   │   ├── services/       # Lógica de negócio
│   │   └── data/           # Armazenamento JSON
│   └── requirements.txt    # Dependências Python
├── frontend/               # Interface React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── services/       # Clientes API
│   │   └── lib/           # Utilitários
│   └── package.json       # Dependências Node.js
└── README.md              # Este arquivo
```

---

**Desenvolvido para facilitar o controle das suas finanças pessoais.**
