# 📊 Dashboard de Programação de Férias

Um dashboard interativo em **Streamlit** para visualizar, filtrar e gerenciar dados de férias de forma simples e intuitiva.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

## ✨ Funcionalidades

- 📅 **Filtro por competência** (MM/YYYY)
- 👤 **Filtro por gestor**
- 🏢 **Filtro por empresa**
- 📊 **Gráficos interativos** (Plotly)
- 📈 **Métricas em tempo real**
- 💾 **Exportar como CSV**
- 🔄 **Suporta .xlsx e .xlsm**

## 🚀 Quick Start

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/dashboard-ferias.git
cd dashboard-ferias

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run app.py
```

A aplicação será aberta em `http://localhost:8501`

### Deploy no Streamlit Cloud

1. Faça push para GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Clique em "New app" e selecione este repositório
4. Escolha `app.py` como arquivo principal
5. Clique em "Deploy" ✅

## 📋 Como usar

1. **Upload da planilha:**
   - Clique em "📂 Faça upload da planilha"
   - Selecione um arquivo `.xlsx` ou `.xlsm`

2. **Filtre os dados:**
   - Use a barra lateral para selecionar competência, gestor e empresa
   - Os gráficos e tabela se atualizam automaticamente

3. **Exporte os dados:**
   - Clique em "📥 Baixar como CSV" para salvar os dados filtrados

## 📁 Estrutura do projeto

```
dashboard-ferias/
├── app.py                          # Aplicação principal
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
└── Modelo_de_Planilha_de_férias.xlsm   # (Opcional) Exemplo de planilha
```

## 🔧 Configuração

Nenhuma configuração adicional é necessária. O dashboard funciona "out of the box"!

## 📊 Exemplo de dados esperados

A planilha deve ter colunas como:
- **Gestor** - Nome do gestor
- **Empresa** - Nome da empresa
- **Empregado** - Nome do colaborador
- **Data Inicio gozo férias** - Data de início (em qualquer formato comum)
- **Dias direito** - Número de dias de férias

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Abra uma **Issue** ou envie um **Pull Request**.

## 📝 Licença

Este projeto está sob licença MIT.

## 📞 Contato

Para dúvidas ou sugestões:
- Abra uma **Issue** no GitHub
- Visite [discuss.streamlit.io](https://discuss.streamlit.io)

---

**Desenvolvido com ❤️ usando [Streamlit](https://streamlit.io)**
