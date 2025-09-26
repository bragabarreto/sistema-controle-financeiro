# Sistema de Controle Financeiro

Um sistema completo de gestão financeira pessoal com processamento inteligente de documentos via IA.

## 🌐 **APLICAÇÃO ONLINE**

### 🚀 **Site Publicado**
- **URL Principal**: https://bragabarreto.github.io/sistema-controle-financeiro/
- **Repositório GitHub**: https://github.com/bragabarreto/sistema-controle-financeiro
- **Status**: ✅ Deploy realizado com sucesso

### 📱 **Acesso Rápido**
A aplicação está **100% funcional** e inclui:
- Interface moderna e responsiva
- Dashboard interativo com gráficos
- Processamento de documentos via IA
- Sistema completo de gestão financeira

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
