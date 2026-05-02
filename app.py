import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os

st.set_page_config(page_title="Gestão Corporativa NCMX", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    :root {
        --primary: #1E40AF;
        --primary-dark: #1E3A8A;
        --accent: #3B82F6;
        --success: #10B981;
        --danger: #EF4444;
        --gray-dark: #1F2937;
        --gray-light: #F9FAFB;
        --border: #E5E7EB;
    }
    
    h1 { color: var(--primary-dark); font-weight: 700; font-size: 2.5rem; margin-bottom: 0.25rem; text-align: center; }
    h2 { color: var(--primary-dark); font-weight: 600; font-size: 1.5rem; border-bottom: 3px solid var(--accent); padding-bottom: 0.75rem; margin-top: 2rem; margin-bottom: 1rem; }
    h3 { color: var(--primary); font-weight: 600; font-size: 1.1rem; }
    
    [data-testid="metric-container"] { background: white; border-radius: 8px; padding: 1rem; border-left: 4px solid var(--accent); box-shadow: 0 2px 8px rgba(30, 64, 175, 0.08); }
    [data-testid="stDataFrame"] { background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); }
    button { background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%) !important; border: none !important; border-radius: 6px !important; color: white !important; font-weight: 600 !important; padding: 0.6rem 1.2rem !important; }
    [data-testid="stSelectbox"], [data-testid="stMultiSelect"] { background: white !important; border-radius: 6px !important; border: 1px solid var(--border) !important; }
    [data-testid="stTabs"] [role="tab"] { background-color: var(--gray-light); border-radius: 6px 6px 0 0; color: var(--gray-dark); font-weight: 600; font-size: 0.95rem; padding: 0.75rem 1.25rem !important; }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] { background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%); color: white; }
</style>
""", unsafe_allow_html=True)

DB_PATH = "ncmx_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados_ferias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            dados BLOB
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qlp_ncmx (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT, codigo REAL, nome TEXT, cargo TEXT, cr TEXT,
            admissao DATE, local_trabalho TEXT, uf_trabalho TEXT,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def salvar_ferias(df):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    import pickle
    dados_blob = pickle.dumps(df)
    cursor.execute("DELETE FROM dados_ferias")
    cursor.execute("INSERT INTO dados_ferias (dados) VALUES (?)", (dados_blob,))
    conn.commit()
    conn.close()

def carregar_ferias():
    init_db()
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT dados FROM dados_ferias LIMIT 1")
        resultado = cursor.fetchone()
        if resultado:
            import pickle
            df = pickle.loads(resultado[0])
            conn.close()
            return df
    except:
        pass
    conn.close()
    return None

def salvar_qlp(df):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM qlp_ncmx")
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO qlp_ncmx (empresa, codigo, nome, cargo, cr, admissao, local_trabalho, uf_trabalho)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (row.get('Empresa'), row.get('Código'), row.get('Nome'), row.get('Cargo'),
              row.get('CR'), row.get('Admissão'), row.get('Local de trabalho'), row.get('UF Trabalho')))
    conn.commit()
    conn.close()

def carregar_qlp():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT empresa, codigo, nome, cargo, cr, admissao, local_trabalho, uf_trabalho FROM qlp_ncmx")
        resultados = cursor.fetchall()
        if resultados:
            df = pd.DataFrame(resultados, columns=['Empresa', 'Código', 'Nome', 'Cargo', 'CR', 'Admissão', 'Local de trabalho', 'UF Trabalho'])
            conn.close()
            return df
    except:
        pass
    conn.close()
    return None

header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
with header_col2:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, rgba(30, 64, 175, 0.05), rgba(59, 130, 246, 0.05)); border-radius: 12px; margin-bottom: 1.5rem;'>
        <h1 style='margin: 0 0 0.25rem 0;'>🏢 Gestão NCMX</h1>
        <p style='color: #6B7280; font-size: 0.95rem; margin: 0; font-weight: 500;'>Dashboard Corporativo Integrado</p>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Férias", "👥 QLP NCMX", "🔗 Sincronização"])

with tab1:
    st.markdown("### 📅 Gestão de Férias")
    
    with st.sidebar:
        st.markdown("#### ⚙️ Férias")
        df_ferias = carregar_ferias()
        if df_ferias is not None and len(df_ferias) > 0:
            st.success(f"✅ {len(df_ferias)} registros")
        else:
            st.info("📂 Nenhum dado")
        
        st.markdown("---")
        uploaded_file = st.file_uploader("📥 Planilha férias", type=["xlsx", "xlsm"], key="uploader_ferias")
        
        if uploaded_file:
            try:
                df_novo = pd.read_excel(uploaded_file, sheet_name="Planilha1", header=1)
                df_novo = df_novo.dropna(axis=1, how='all')
                df_novo = df_novo.loc[:, ~df_novo.columns.str.contains('^Unnamed')]
                df_novo.columns = df_novo.columns.str.strip()
                df_novo = df_novo.dropna(how='all')
                
                data_columns = [col for col in df_novo.columns if 'PROGRAMAÇÃO' in col and 'gozo' in col.lower()]
                if not data_columns:
                    data_columns = [col for col in df_novo.columns if 'gozo' in col.lower()]
                
                if data_columns:
                    coluna_data = data_columns[0]
                    df_novo[coluna_data] = pd.to_datetime(df_novo[coluna_data], errors='coerce', dayfirst=True)
                    df_novo = df_novo.dropna(subset=[coluna_data])
                    df_novo["Competência"] = df_novo[coluna_data].dt.strftime("%m/%Y")
                    
                    salvar_ferias(df_novo)
                    st.success("✅ Sincronizado!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ {str(e)}")
    
    df_ferias = carregar_ferias()
    
    if df_ferias is not None and len(df_ferias) > 0:
        col1, col2, col3 = st.columns([1.2, 1, 1])
        
        with col1:
            competencias = sorted(df_ferias["Competência"].unique())
            competencia_selecionada = st.selectbox("📅 Competência", competencias, key="comp_ferias")
        
        with col2:
            if "Gestor" in df_ferias.columns:
                gestores = sorted(df_ferias["Gestor"].dropna().unique())
                gestor_selecionado = st.multiselect("👤 Gestor", gestores, default=gestores[:3] if len(gestores) > 3 else gestores, key="gestor_ferias")
            else:
                gestor_selecionado = None
        
        with col3:
            if "Centro de Resultado" in df_ferias.columns:
                crs = sorted(df_ferias["Centro de Resultado"].dropna().unique())
                cr_selecionado = st.multiselect("🏢 CR", crs, default=crs, key="cr_ferias")
            else:
                cr_selecionado = None
        
        df_filt = df_ferias[df_ferias["Competência"] == competencia_selecionada].copy()
        
        if gestor_selecionado and "Gestor" in df_filt.columns:
            df_filt = df_filt[df_filt["Gestor"].isin(gestor_selecionado)]
        
        if cr_selecionado and "Centro de Resultado" in df_filt.columns:
            df_filt = df_filt[df_filt["Centro de Resultado"].isin(cr_selecionado)]
        
        st.markdown("---")
        st.markdown("### 📊 Indicadores")
        
        met_col1, met_col2, met_col3, met_col4 = st.columns(4)
        
        with met_col1:
            st.metric("👥 Colaboradores", len(df_filt))
        
        with met_col2:
            if "Dias direito" in df_filt.columns:
                dias_col = pd.to_numeric(df_filt["Dias direito"], errors='coerce')
                st.metric("📆 Dias", f"{dias_col.sum():.0f}")
        
        with met_col3:
            if "Gestor" in df_filt.columns:
                st.metric("👨‍💼 Gestores", df_filt["Gestor"].nunique())
        
        with met_col4:
            if "Centro de Resultado" in df_filt.columns:
                st.metric("🏢 CRs", df_filt["Centro de Resultado"].nunique())
        
        st.markdown("---")
        st.markdown("### 📈 Análises")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            if "Gestor" in df_filt.columns and len(df_filt) > 0:
                st.bar_chart(df_filt["Gestor"].value_counts().head(8), color="#3B82F6")
        
        with chart_col2:
            if "Centro de Resultado" in df_filt.columns and len(df_filt) > 0:
                st.bar_chart(df_filt["Centro de Resultado"].value_counts(), color="#10B981")
        
        st.markdown("---")
        st.markdown(f"### 📋 Dados - {competencia_selecionada}")
        
        colunas_display = [col for col in df_filt.columns if col != "Competência"]
        df_display = df_filt[colunas_display].copy()
        
        for col in df_display.columns:
            if pd.api.types.is_datetime64_any_dtype(df_display[col]):
                df_display[col] = df_display[col].dt.strftime("%d/%m/%Y")
        
        st.dataframe(df_display, use_container_width=True, height=300)
    else:
        st.info("📂 Carregue a planilha de férias no sidebar")

with tab2:
    st.markdown("### 👥 QLP NCMX - Gestão de Pessoal")
    
    with st.sidebar:
        st.markdown("#### ⚙️ QLP NCMX")
        df_qlp = carregar_qlp()
        
        if df_qlp is not None and len(df_qlp) > 0:
            st.success(f"✅ {len(df_qlp)} registros")
        else:
            st.info("📂 Nenhum dado")
        
        st.markdown("---")
        uploaded_qlp = st.file_uploader("📥 Planilha QLP", type=["xlsx", "xlsm"], key="uploader_qlp")
        
        if uploaded_qlp:
            try:
                df_qlp_novo = pd.read_excel(uploaded_qlp)
                salvar_qlp(df_qlp_novo)
                st.success("✅ Sincronizado!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ {str(e)}")
    
    df_qlp = carregar_qlp()
    
    if df_qlp is not None and len(df_qlp) > 0:
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            empresas = sorted(df_qlp["Empresa"].unique())
            empresa_selecionada = st.selectbox("🏢 Empresa", empresas, key="empresa_qlp")
        
        with col2:
            crs = sorted(df_qlp[df_qlp["Empresa"] == empresa_selecionada]["CR"].unique())
            cr_selecionado = st.multiselect("🏢 CR", crs, default=crs, key="cr_qlp")
        
        with col3:
            ufs = sorted(df_qlp["UF Trabalho"].unique())
            uf_selecionado = st.multiselect("📍 UF", ufs, default=ufs, key="uf_qlp")
        
        df_qlp_filt = df_qlp[df_qlp["Empresa"] == empresa_selecionada].copy()
        
        if cr_selecionado:
            df_qlp_filt = df_qlp_filt[df_qlp_filt["CR"].isin(cr_selecionado)]
        
        if uf_selecionado:
            df_qlp_filt = df_qlp_filt[df_qlp_filt["UF Trabalho"].isin(uf_selecionado)]
        
        st.markdown("---")
        st.markdown("### 📊 Indicadores")
        
        met_col1, met_col2, met_col3, met_col4 = st.columns(4)
        
        with met_col1:
            st.metric("👥 Total", len(df_qlp_filt))
        
        with met_col2:
            st.metric("🏢 CRs", df_qlp_filt["CR"].nunique())
        
        with met_col3:
            st.metric("📍 Estados", df_qlp_filt["UF Trabalho"].nunique())
        
        with met_col4:
            st.metric("🏪 Locais", df_qlp_filt["Local de trabalho"].nunique())
        
        st.markdown("---")
        st.markdown("### 📈 Análises")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.bar_chart(df_qlp_filt["CR"].value_counts(), color="#3B82F6")
        
        with chart_col2:
            st.bar_chart(df_qlp_filt["UF Trabalho"].value_counts(), color="#10B981")
        
        st.markdown("---")
        st.markdown("### ✏️ Dados - Edição")
        
        st.info("💡 Edite os dados diretamente na tabela")
        
        edited_data = st.data_editor(
            df_qlp_filt.reset_index(drop=True),
            use_container_width=True,
            height=300,
            key="qlp_editor"
        )
        
        if edited_data is not None and not edited_data.equals(df_qlp_filt.reset_index(drop=True)):
            salvar_qlp(edited_data)
            st.success("✅ Alterações salvas!")
            st.rerun()
    else:
        st.info("📂 Carregue a planilha QLP NCMX no sidebar")

with tab3:
    st.markdown("### 🔗 Sincronização CR/Centro de Resultado")
    
    df_ferias = carregar_ferias()
    df_qlp = carregar_qlp()
    
    if df_ferias is None or len(df_ferias) == 0:
        st.error("❌ Carregue férias primeiro")
    elif df_qlp is None or len(df_qlp) == 0:
        st.error("❌ Carregue QLP NCMX primeiro")
    else:
        st.markdown("---")
        st.markdown("### 📊 Status da Sincronização")
        
        crs_ferias = set(df_ferias["Centro de Resultado"].dropna().unique())
        crs_qlp = set(df_qlp["CR"].unique())
        
        crs_em_ambas = crs_ferias & crs_qlp
        crs_so_ferias = crs_ferias - crs_qlp
        crs_so_qlp = crs_qlp - crs_ferias
        
        sync_col1, sync_col2, sync_col3, sync_col4 = st.columns(4)
        
        with sync_col1:
            st.metric("✅ Sincronizados", len(crs_em_ambas))
        
        with sync_col2:
            st.metric("⚠️ Só Férias", len(crs_so_ferias))
        
        with sync_col3:
            st.metric("⚠️ Só QLP", len(crs_so_qlp))
        
        with sync_col4:
            taxa = (len(crs_em_ambas) / max(len(crs_ferias), len(crs_qlp)) * 100) if max(len(crs_ferias), len(crs_qlp)) > 0 else 0
            st.metric("📊 Taxa", f"{taxa:.1f}%")
        
        st.markdown("---")
        st.markdown("### 📋 Detalhes")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### ✅ CRs Sincronizados")
            st.write(", ".join(sorted(crs_em_ambas)) if crs_em_ambas else "Nenhum")
        
        with col2:
            st.markdown("#### ⚠️ Só em Férias")
            st.write(", ".join(sorted(crs_so_ferias)) if crs_so_ferias else "Nenhum")
        
        with col3:
            st.markdown("#### ⚠️ Só em QLP")
            st.write(", ".join(sorted(crs_so_qlp)) if crs_so_qlp else "Nenhum")
        
        st.markdown("---")
        st.markdown("### 📊 Comparação por CR")
        
        comparacao = []
        todos_crs = sorted(set(crs_ferias | crs_qlp))
        
        for cr in todos_crs:
            ferias_count = len(df_ferias[df_ferias["Centro de Resultado"] == cr])
            qlp_count = len(df_qlp[df_qlp["CR"] == cr])
            status = "✅ OK" if (ferias_count > 0 and qlp_count > 0) else "⚠️ Desincronizado"
            
            comparacao.append({"CR": cr, "Férias": ferias_count, "QLP": qlp_count, "Status": status})
        
        df_comparacao = pd.DataFrame(comparacao)
        st.dataframe(df_comparacao, use_container_width=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #9CA3AF; font-size: 0.85rem; padding: 1rem 0;'>
    <p style='margin: 0;'>Gestão Corporativa NCMX © 2026</p>
    <p style='margin: 0;'>Férias | QLP NCMX | Sincronização Integrada</p>
</div>
""", unsafe_allow_html=True)
