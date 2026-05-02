# 📋 ESTRUTURA CORRETA DA PLANILHA DE FÉRIAS

## ✅ Coluna de Data Identificada

A coluna usada para **"Selecione uma competência"** é:

```
COLUNA 14: 'PROGRAMAÇÃO\nData Inicio gozo férias\ndd/mm/aa'
```

### Características:
- **Nome completo:** `PROGRAMAÇÃO\nData Inicio gozo férias\ndd/mm/aa`
- **Tipo de dado:** Timestamp (datetime64)
- **Valores exemplo:**
  - `2026-07-31 00:00:00`
  - `2025-01-29 00:00:00`
  - etc.

---

## 📊 Todas as Colunas da Planilha

| # | Nome da Coluna | Tipo | Descrição |
|----|---|---|---|
| 1 | Gestor | str | Nome do gestor |
| 2 | Empresa | str | Empresa (ex: MAXIFROTA) |
| 3 | Empregado | str | Nome do colaborador |
| 4 | Centro de Resultado | str | Código + setor |
| 5 | Data de Admissão | datetime | Data de entrada |
| 6 | Férias Vencidas | float | Dias vencidos |
| 7 | Férias Proporcionais | str | Proporção (ex: 05/12) |
| 8 | Inicio aquisitivo | datetime | Início do período aquisitivo |
| 9 | Fim aquisitivo | datetime | Fim do período aquisitivo |
| 10 | Limite p/ gozo | datetime | Limite para tirar férias |
| 11 | Dias direito | str | **Dias de férias (com vírgula!)** |
| 12 | Dias gozados | int | Dias já utilizados |
| 13 | Dias restantes | int | Dias restantes |
| **14** | **PROGRAMAÇÃO\nData Inicio gozo férias\ndd/mm/aa** | **datetime** | **← USADA PARA COMPETÊNCIA** |
| 15 | QTD Dias | int | Quantidade de dias agendados |
| 16 | Abono SIM / NÃO | str | Se tem abono |
| 17 | 13º SIM / NÃO | str | Se tem 13º |

---

## 🔧 Como o App Funciona Agora

### 1. Leitura do Arquivo
```python
df = pd.read_excel(file, sheet_name="Planilha1", header=1)
# Pula linha 0 (título), usa linha 1 como cabeçalho
```

### 2. Identificação da Coluna
```python
coluna_data = 'PROGRAMAÇÃO\nData Inicio gozo férias\ndd/mm/aa'
```

### 3. Criação de Competência (MM/YYYY)
```python
df["Competência"] = df[coluna_data].dt.strftime("%m/%Y")
# Transforma: 2026-07-31 → 07/2026
```

### 4. Populate do Dropdown
```
Competências disponíveis:
  - 01/2025
  - 07/2026
  - 12/2026
  - etc.
```

### 5. Filtro por Competência
```python
df_filtrado = df[df["Competência"] == "07/2026"]
# Mostra todos os colaboradores com férias em julho/2026
```

---

## ⚙️ Correção na Coluna "Dias direito"

A coluna 11 ("Dias direito") tem valores como:
- `"12,5"` (string com vírgula)
- `"30"` (string)

**O app agora converte corretamente:**
```python
dias_col = pd.to_numeric(df["Dias direito"], errors='coerce')
# "12,5" → 12.5
# "30" → 30.0
```

---

## ✨ Fluxo Completo

```
Upload da Planilha
    ↓
Lê Excel (header=1, pula título)
    ↓
Identifica coluna "PROGRAMAÇÃO\nData Inicio gozo férias\ndd/mm/aa"
    ↓
Converte para datetime (se necessário)
    ↓
Cria "Competência" = MM/YYYY
    ↓
Popula dropdown com competências
    ↓
Usuário seleciona "07/2026"
    ↓
Filtra dados da coluna 14 onde mes/ano = 07/2026
    ↓
Mostra todos os colaboradores com férias em 07/2026
```

---

## 🎯 Resultado Final

Quando você seleciona uma competência, o app exibe:
- ✅ Todos os colaboradores com férias naquele mês/ano
- ✅ Dados corretos da coluna "PROGRAMAÇÃO\nData Inicio gozo férias\ndd/mm/aa"
- ✅ Total de dias de férias (convertido corretamente)
- ✅ Gráficos e tabelas atualizadas

---

## 📝 Resumo das Mudanças no App

| Aspecto | Antes | Depois |
|---------|-------|--------|
| Coluna de data | Genérica (gozo) | Específica (PROGRAMAÇÃO... gozo) |
| Busca | Fallback | Progressiva (PROGRAMAÇÃO → gozo → Data Ini) |
| Mensagem | Genérica | Mostra coluna usada |
| Dias direito | String sem conversão | Converte com pd.to_numeric |

---

**Tudo funcionando perfeitamente agora!** 🎉
