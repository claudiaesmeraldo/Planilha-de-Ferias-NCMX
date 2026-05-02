import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

# ======== CONFIGURAÇÃO DA PÁGINA ========
st.set_page_config(
    page_title="Dashboard de Férias 2026",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======== ESTILOS ========
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Dashboard de Programação de Férias 2026")
st.markdown("""
Visualize e filtre as férias previstas por **competência (MM/AAAA)**, 
**gestor**, **empresa** e outras dimensões. Com base na data de início do gozo de férias.
""")

# ======== UPLOAD DO ARQUIVO ========
uploaded_file = st.file_uploader(
    "📂 Faça upload da planilha de férias (.xlsx ou .xlsm)",
    type=["xlsx", "xlsm"]
)

if uploaded_file:
    try:
        # ======== LEITURA E LIMPEZA DOS DADOS ========
        # Pula linha 0 (título) e usa linha 1 como cabeçalho
        df = pd.read_excel(uploaded_file, sheet_name="Planilha1", header=1)
        
        # Remove colunas vazias e colunas sem nome
        df = df.dropna(axis=1, how='all')
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # Padroniza nomes das colunas
        df.columns = df.columns.str.strip()
        
        # Remove linhas completamente vazias
        df = df.dropna(how='all')
        
        # Identifica a coluna de data (pode ter variações de nome)
        data_columns = [col for col in df.columns if 'Data' in col and ('Ini' in col or 'data' in col.lower())]
        
        if not data_columns:
            st.error("❌ Nenhuma coluna de data de início encontrada!")
            st.stop()
        
        coluna_data = data_columns[0]
        
        # Converte para datetime
        df[coluna_data] = pd.to_datetime(
            df[coluna_data],
            errors='coerce',
            dayfirst=True
        )
        
        # Remove registros sem data válida
        df_clean = df.dropna(subset=[coluna_data]).copy()
        
        # Cria coluna de competência (MM/YYYY)
        df_clean["Competência"] = df_clean[coluna_data].dt.strftime("%m/%Y")
        
        # ======== SIDEBAR - FILTROS ========
        st.sidebar.header("🔍 Filtros")
        
        # Filtro de Competência
        competencias = sorted(df_clean["Competência"].unique())
        competencia_selecionada = st.sidebar.selectbox(
            "📅 Selecione a competência",
            competencias,
            index=0
        )
        
        # Filtro de Gestor (se disponível)
        if "Gestor" in df_clean.columns:
            gestores = sorted(df_clean["Gestor"].dropna().unique())
            gestor_selecionado = st.sidebar.multiselect(
                "👤 Gestor(es)",
                gestores,
                default=gestores
            )
        else:
            gestor_selecionado = None
        
        # Filtro de Empresa (se disponível)
        if "Empresa" in df_clean.columns:
            empresas = sorted(df_clean["Empresa"].dropna().unique())
            empresa_selecionada = st.sidebar.multiselect(
                "🏢 Empresa(s)",
                empresas,
                default=empresas
            )
        else:
            empresa_selecionada = None
        
        # ======== APLICAR FILTROS ========
        df_filtrado = df_clean[df_clean["Competência"] == competencia_selecionada].copy()
        
        if gestor_selecionado and "Gestor" in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado["Gestor"].isin(gestor_selecionado)]
        
        if empresa_selecionada and "Empresa" in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado["Empresa"].isin(empresa_selecionada)]
        
        # ======== MÉTRICAS PRINCIPAIS ========
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "👥 Total de Colaboradores",
                len(df_filtrado),
                delta=f"de {len(df_clean)} total"
            )
        
        with col2:
            if "Dias direito" in df_filtrado.columns:
                dias_totais = df_filtrado["Dias direito"].sum()
                st.metric("📆 Dias Totais", f"{dias_totais:.0f}")
            else:
                st.metric("📆 Dias Totais", "N/A")
        
        with col3:
            if "Gestor" in df_filtrado.columns:
                num_gestores = df_filtrado["Gestor"].nunique()
                st.metric("👥 Gestores", num_gestores)
            else:
                st.metric("👥 Gestores", "N/A")
        
        with col4:
            if "Empresa" in df_filtrado.columns:
                num_empresas = df_filtrado["Empresa"].nunique()
                st.metric("🏢 Empresas", num_empresas)
            else:
                st.metric("🏢 Empresas", "N/A")
        
        # ======== GRÁFICOS ========
        st.subheader("📈 Análise Visual")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            if "Gestor" in df_filtrado.columns and len(df_filtrado) > 0:
                chart_data = df_filtrado["Gestor"].value_counts().head(10)
                fig = px.bar(
                    x=chart_data.index,
                    y=chart_data.values,
                    title="👤 Top 10 Gestores com mais férias agendadas",
                    labels={"x": "Gestor", "y": "Quantidade"}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col_chart2:
            if "Empresa" in df_filtrado.columns and len(df_filtrado) > 0:
                chart_data = df_filtrado["Empresa"].value_counts().head(10)
                fig = px.pie(
                    values=chart_data.values,
                    names=chart_data.index,
                    title="🏢 Distribuição por Empresa"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # ======== TABELA DE DADOS ========
        st.subheader(f"👥 Colaboradores - Competência {competencia_selecionada}")
        st.write(f"**Total de registros:** {len(df_filtrado)}")
        
        # Seleciona colunas principais para exibição
        colunas_display = [col for col in df_filtrado.columns if col != "Competência"]
        
        # Formata a tabela
        df_display = df_filtrado[colunas_display].copy()
        
        # Converte datas para string formatado
        for col in df_display.columns:
            if pd.api.types.is_datetime64_any_dtype(df_display[col]):
                df_display[col] = df_display[col].dt.strftime("%d/%m/%Y")
        
        st.dataframe(
            df_display,
            use_container_width=True,
            height=400
        )
        
        # ======== DOWNLOAD DOS DADOS FILTRADOS ========
        st.subheader("💾 Exportar Dados")
        
        csv = df_display.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Baixar como CSV",
            data=csv,
            file_name=f"ferias_competencia_{competencia_selecionada.replace('/', '_')}.csv",
            mime="text/csv"
        )
        
        # ======== INFORMAÇÕES GERAIS ========
        with st.expander("ℹ️ Informações sobre os dados"):
            st.write(f"""
            - **Total de registros na planilha:** {len(df_clean)}
            - **Período coberto:** De {df_clean[coluna_data].min().strftime('%m/%Y')} a {df_clean[coluna_data].max().strftime('%m/%Y')}
            - **Colunas disponíveis:** {len(df_filtrado.columns)}
            """)
    
    except Exception as e:
        st.error("❌ Erro ao processar o arquivo.")
        st.write(f"**Detalhes:** {str(e)}")
        with st.expander("🔧 Debug Info"):
            import traceback
            st.code(traceback.format_exc())

else:
    st.info("⬆️ Faça o upload da planilha para visualizar o dashboard.")
    st.markdown("""
    ### 📋 O que este dashboard faz:
    ✅ Lê planilhas .xlsx e .xlsm  
    ✅ Filtra por competência (MM/YYYY)  
    ✅ Filtra por gestor e empresa  
    ✅ Exibe métricas e gráficos  
    ✅ Permite exportar dados filtrados  
    ✅ Trata automaticamente datas em diferentes formatos  
    """)
