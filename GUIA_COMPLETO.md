# 📊 Dashboard de Férias - Guia Completo

## ✨ Melhorias Implementadas

Este dashboard foi **otimizado** para:
- ✅ Ler corretamente a estrutura da sua planilha (.xlsm)
- ✅ Filtrar por competência, gestor e empresa
- ✅ Exibir métricas (total de colaboradores, dias, gestores, empresas)
- ✅ Mostrar gráficos interativos (Plotly)
- ✅ Exportar dados filtrados em CSV
- ✅ Tratar automaticamente datas em vários formatos
- ✅ Interface responsiva e amigável

---

## 🚀 SETUP LOCAL

### 1️⃣ Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes)

### 2️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 3️⃣ Executar localmente

```bash
streamlit run app.py
```

A aplicação abrirá em `http://localhost:8501`

---

## 🌐 PUBLICAR NO GITHUB

### 1️⃣ Criar repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique em **"New"** para criar novo repositório
3. Nome: `dashboard-ferias`
4. Descrição: `Dashboard de Programação de Férias em Streamlit`
5. Deixe **Public** (para Streamlit Cloud)
6. Clique em **"Create repository"**

### 2️⃣ Clonar e fazer upload dos arquivos

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/dashboard-ferias.git
cd dashboard-ferias

# Copie os arquivos para a pasta
# - app.py
# - requirements.txt
# - Modelo_de_Planilha_de_férias.xlsm (opcional)

# Adicione os arquivos ao Git
git add .
git commit -m "feat: Initial commit - Dashboard de Férias"
git push origin main
```

### 3️⃣ Estrutura do repositório

```
dashboard-ferias/
├── app.py                                 # Aplicação principal
├── requirements.txt                       # Dependências Python
├── Modelo_de_Planilha_de_férias.xlsm     # (Opcional) Planilha de exemplo
└── README.md                              # Este arquivo
```

---

## ☁️ PUBLICAR NO STREAMLIT CLOUD

### 1️⃣ Acessar Streamlit Community Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em **"Sign up with GitHub"**
3. Autorize o Streamlit a acessar seus repositórios

### 2️⃣ Criar nova aplicação

1. Clique em **"New app"**
2. Preencha os dados:
   - **Repository:** `SEU_USUARIO/dashboard-ferias`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Clique em **"Deploy"** ✅

### 3️⃣ URL da sua aplicação

Após o deploy, você receberá uma URL como:
```
https://dashboard-ferias-RANDOMSTRING.streamlit.app
```

---

## 🔧 VARIÁVEIS DE AMBIENTE (Opcional)

Se precisar de configurações adicionais, crie um arquivo `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
```

---

## 📋 PRÓXIMAS EVOLUÇÕES (ROADMAP)

Funcionalidades que podem ser adicionadas facilmente:

### 🔄 Prioritário
- [ ] KPI: Gráfico de férias por mês (timeline)
- [ ] Filtro por Centro de Resultado
- [ ] Alertas para prazos (férias vencendo)

### ⭐ Médio Prazo
- [ ] Calendário visual de férias
- [ ] Relatório em PDF
- [ ] Login/autenticação (proteger acesso)
- [ ] Integração com API de RH

### 🚀 Longo Prazo
- [ ] Multi-upload (várias planilhas)
- [ ] Comparação entre períodos
- [ ] Dashboard de auditoria (quem viu o quê)
- [ ] Webhook para notificações

---

## ❓ DÚVIDAS FREQUENTES

### P: Posso usar minha própria planilha?
**R:** Sim! Basta fazer upload. Certifique-se de que:
- Tem uma coluna com datas de início de férias
- Tem nomes de colunas claros na linha 1 ou 2
- Salve em .xlsx ou .xlsm

### P: Como adicionar mais filtros?
**R:** Edite a seção de filtros no `app.py` e adicione:
```python
novo_filtro = st.sidebar.multiselect(
    "🔍 Novo Filtro",
    df_filtrado["coluna"].unique()
)
```

### P: Posso usar um banco de dados em vez de Excel?
**R:** Sim! Você pode conectar a um SQL Server, PostgreSQL ou Google Sheets usando bibliotecas como `sqlalchemy` ou `gspread`.

### P: Como fazer backup automático?
**R:** Configure o Streamlit Cloud para sincronizar automaticamente com o GitHub. Qualquer commit atualiza a aplicação.

---

## 📞 SUPORTE

- Documentação Streamlit: [docs.streamlit.io](https://docs.streamlit.io)
- GitHub Issues: Crie uma issue no repositório
- Comunidade: [discuss.streamlit.io](https://discuss.streamlit.io)

---

## 📄 LICENSE

Este projeto está sob licença MIT. Sinta-se livre para usar e modificar!

---

**Desenvolvido com ❤️ usando Streamlit**
