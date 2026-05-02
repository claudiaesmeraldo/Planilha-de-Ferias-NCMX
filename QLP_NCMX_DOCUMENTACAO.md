# 🏢 Funcionalidade QLP NCMX - Documentação Completa

## ✨ O Que É QLP NCMX?

**QLP NCMX** é a nova função de gestão de pessoal que permite:
- ✅ Gerenciar dados de colaboradores (Nome, Cargo, CR, Local, UF)
- ✅ Editar campos diretamente na interface
- ✅ Sincronizar dados de **Centro de Resultado (CR)** entre férias e pessoal
- ✅ Validar consistência dos dados
- ✅ Analisar correlações

---

## 📊 Estrutura de Dados QLP NCMX

### Colunas da Planilha

| Coluna | Tipo | Descrição | Editável |
|--------|------|-----------|----------|
| **Empresa** | Texto | Nome da empresa | ✅ Sim |
| **Código** | Número | ID do colaborador | ❌ Não |
| **Nome** | Texto | Nome completo | ✅ Sim |
| **Cargo** | Texto | Cargo/Função | ✅ Sim |
| **CR** | Texto | Centro de Resultado | ✅ Sim |
| **Admissão** | Data | Data de admissão | ✅ Sim |
| **Local de trabalho** | Texto | Cidade/Local | ✅ Sim |
| **UF Trabalho** | Texto | Estado (sigla) | ✅ Sim |

---

## 🎯 As 3 Abas do Dashboard

### 1️⃣ **Aba FÉRIAS** (📊)

**Funcionalidades:**
- Gerenciar programação de férias
- Filtrar por competência, gestor, CR
- Visualizar métricas e gráficos
- Sincronizar dados

**Filtros disponíveis:**
```
📅 Competência → Mês/Ano das férias
👤 Gestor → Nome do gestor
🏢 CR → Centro de Resultado
```

**Métricas exibidas:**
```
👥 Colaboradores → Total de pessoas
📆 Dias → Dias totais de férias
👨‍💼 Gestores → Quantidade de gestores
🏢 CRs → Quantidade de centros de resultado
```

---

### 2️⃣ **Aba QLP NCMX** (👥)

**Funcionalidades:**
- ✅ Visualizar dados de pessoal
- ✅ **EDITAR campos diretamente**
- ✅ Filtrar por empresa, CR, UF
- ✅ Sincronizar com férias

**Filtros disponíveis:**
```
🏢 Empresa → Empresa selecionada
🏢 CR → Centro de Resultado
📍 UF → Estado de trabalho
```

**Métricas exibidas:**
```
👥 Total → Total de colaboradores
🏢 CRs → Centros de resultado únicos
📍 Estados → Estados únicos
🏪 Locais → Locais de trabalho únicos
```

**Como Editar:**
1. Na tabela abaixo, clique em qualquer célula
2. Edite o valor desejado
3. As alterações são salvas automaticamente ✅
4. Dados sincronizam com o banco de dados

---

### 3️⃣ **Aba SINCRONIZAÇÃO** (🔗)

**Funcionalidades:**
- ✅ Validar consistência entre férias e QLP
- ✅ Identificar CRs desincronizados
- ✅ Taxa de sincronização
- ✅ Análise comparativa

**Métricas de Sincronização:**
```
✅ Sincronizados → CRs em ambas as planilhas
⚠️ Só Férias → CRs só em férias
⚠️ Só QLP → CRs só em QLP
📊 Taxa → Percentual de sincronização
```

**Tabela Comparativa:**
```
CR | Férias | QLP | Status
---|--------|-----|--------
AA |   12   |  15 | ⚠️ Desincronizado
BB |   8    |   8 | ✅ OK
CC |   0    |   5 | ⚠️ Desincronizado
```

**Status de Sincronização:**
- ✅ **OK**: CR tem dados em férias E em QLP
- ⚠️ **Desincronizado**: CR falta em uma das planilhas

---

## 🔄 Como Funciona a Sincronização

### Fluxo de Dados

```
ARQUIVO QLP.xlsx
     ↓
UPLOAD
     ↓
PROCESSAMENTO
     ↓
BANCO SQLite
     ↓
TAB QLP NCMX (Edição possível)
     ↓
SINCRONIZAÇÃO COM FÉRIAS
     ↓
TAB SINCRONIZAÇÃO (Validação)
```

### Banco de Dados Integrado

```
ncmx_data.db
├── Tabela: dados_ferias
│   ├── id (PK)
│   ├── data_upload
│   └── dados (BLOB - DataFrame)
│
└── Tabela: qlp_ncmx
    ├── id (PK)
    ├── empresa
    ├── codigo
    ├── nome
    ├── cargo
    ├── cr ← CAMPO CRÍTICO PARA SINCRONIZAÇÃO
    ├── admissao
    ├── local_trabalho
    ├── uf_trabalho
    └── data_atualizacao
```

---

## 📋 Exemplo de Uso Prático

### Cenário 1: Novo Colaborador

**Passos:**
1. Atualize a planilha QLP com novo colaborador
2. Faça upload na **Aba QLP NCMX**
3. Verifique se o **CR está correto**
4. Vá para **Aba Sincronização** para validar
5. Crie programação de férias na **Aba Férias**

### Cenário 2: Atualizar CR de Colaborador

**Passos:**
1. Vá para **Aba QLP NCMX**
2. Encontre o colaborador na tabela
3. **Clique na célula do CR** e altere
4. Dados salvos automaticamente ✅
5. Verifique sincronização na **Aba Sincronização**

### Cenário 3: Validar Consistência

**Passos:**
1. Vá para **Aba Sincronização**
2. Observe as **métricas** no topo
3. Analise a **tabela comparativa**
4. Corrija discrepâncias editando em **QLP NCMX**
5. Confirme a sincronização

---

## 🛠️ Funcionalidades Técnicas

### Edição de Dados

```python
# A tabela é editável usando st.data_editor
edited_data = st.data_editor(
    df_qlp_filt.reset_index(drop=True),
    use_container_width=True,
    height=300,
    key="qlp_editor"
)

# Automaticamente detecta mudanças e salva
if edited_data is not None and not edited_data.equals(original):
    salvar_qlp(edited_data)
```

### Sincronização Automática

```python
# Compara CRs entre férias e QLP
crs_ferias = set(df_ferias["Centro de Resultado"].unique())
crs_qlp = set(df_qlp["CR"].unique())

# Calcula interseção
crs_sincronizados = crs_ferias & crs_qlp
taxa_sinc = (len(crs_sincronizados) / max(len(crs_ferias), len(crs_qlp))) * 100
```

---

## 📱 Layout Visual

### Tab QLP NCMX - Estrutura

```
┌─────────────────────────────────────────────────────────┐
│ 👥 QLP NCMX - Gestão de Pessoal                        │
├─────────────────────────────────────────────────────────┤
│ Filtros Compactos                                       │
│ [🏢 Empresa] [🏢 CR] [📍 UF]                           │
├─────────────────────────────────────────────────────────┤
│ 📊 Indicadores                                          │
│ [👥 Total] [🏢 CRs] [📍 Estados] [🏪 Locais]          │
├─────────────────────────────────────────────────────────┤
│ 📈 Análises (Gráficos)                                 │
│ [Gráfico CR]          [Gráfico UF]                     │
├─────────────────────────────────────────────────────────┤
│ ✏️ Dados - Edição                                      │
│ [TABELA EDITÁVEL - Clique para editar]                 │
│ Empresa | Código | Nome | Cargo | CR | ... (colunas)  │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 Boas Práticas

### ✅ O QUE FAZER

- ✅ Manter CRs consistentes entre sistemas
- ✅ Atualizar QLP sempre que houver movimento de pessoal
- ✅ Validar sincronização mensalmente
- ✅ Fazer backup dos dados
- ✅ Documentar alterações importantes

### ❌ O QUE EVITAR

- ❌ Usar CRs diferentes para o mesmo colaborador
- ❌ Deixar campos vazios sem motivo
- ❌ Atualizar apenas uma planilha
- ❌ Alterar campos imutáveis (Código)
- ❌ Duplicar registros

---

## 🚀 Deploy no GitHub + Streamlit Cloud

### Comando para atualizar:

```bash
git add app.py requirements.txt
git commit -m "feat: Adicionar funcionalidade QLP NCMX com sincronização"
git push origin main
```

### O que acontece:
1. Streamlit Cloud detecta mudanças
2. Reconstrui automaticamente (~2-3 min)
3. Nova funcionalidade ativa! 🎉

---

## 📊 Dados de Exemplo

### Estrutura de Entrada (QLP)

```
Empresa    | Código | Nome           | Cargo      | CR  | Admissão   | Local       | UF
-----------|--------|----------------|-----------|-----|------------|-------------|----
MAXIFROTA  | 340    | João Silva     | Gerente    | AA  | 2020-05-15 | SALVADOR    | BA
MAXIFROTA  | 5      | Maria Santos   | Analista   | BB  | 2019-03-22 | SALVADOR    | BA
MAXIFROTA  | 587    | Pedro Costa    | Supervisor | AA  | 2021-08-10 | RECIFE      | PE
```

### Estrutura de Saída (Sincronização)

```
CR | Férias | QLP | Status
---|--------|-----|--------
AA |   20   |  22 | ✅ OK
BB |   15   |  15 | ✅ OK
CC |    0   |   5 | ⚠️ Desincronizado
DD |   10   |   0 | ⚠️ Desincronizado
```

---

## 💡 Dicas de Uso

1. **Antes de editar**: Faça backup da planilha
2. **Validar sempre**: Use Aba Sincronização regularmente
3. **Atualizar CRs**: Mantenha estrutura organizacional atual
4. **Comunicar mudanças**: Avise equipe sobre alterações importantes
5. **Revisar dados**: Confira dados importados antes de usar

---

## 📞 Suporte & Troubleshooting

### Problema: "Dados não sincronizam"
**Solução**: Verifique se CRs estão escritos igualmente em ambas planilhas

### Problema: "Alterações não salvam"
**Solução**: Aguarde 2-3 segundos após editar, o salvamento é automático

### Problema: "Taxa de sincronização baixa"
**Solução**: Atualize CRs na planilha QLP para corresponder com férias

### Problema: "Tabela não aparece editável"
**Solução**: Recarregue a página ou acesse via novo navegador

---

**Tudo funcionando perfeitamente!** ✅

Sistema pronto para gestão integrada de férias e QLP NCMX com sincronização automática. 🎉
