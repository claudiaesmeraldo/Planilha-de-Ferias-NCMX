import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from io import BytesIO
import os

# ======== CONFIGURAÇÃO DA PÁGINA ========
st.set_page_config(page_title="Dashboard de Férias 2026", layout="wide", initial_sidebar_state="expanded")

# ======== ESTILO CSS ========
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', system-ui, sans-serif !important; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%); border-right: 1px solid #e2e8f0; }
[data-testid="stMetric"] { background: #fff; border-radius: 10px; padding: 16px 18px; box-shadow: 0 1px 3px rgba(0,0,0,.06); border: 1px solid #f1f5f9; }
[data-testid="stMetric"] label { font-size: .65rem !important; font-weight: 600 !important; color: #94a3b8 !important; text-transform: uppercase; }
[data-testid="stMetric"] [data-testid="stMetricValue"] { font-size: 1.5rem !important; font-weight: 800 !important; color: #0f172a !important; }
.stButton button { border-radius: 6px; font-weight: 600; font-size: .75rem; }
h1 { font-size: 1.4rem !important; font-weight: 800 !important; color: #0f172a !important; }
h3 { font-size: .95rem !important; font-weight: 700 !important; color: #334155 !important; }
[data-testid="stDataEditor"] { border-radius: 10px; overflow: hidden; border: 1px solid #f1f5f9; box-shadow: 0 1px 3px rgba(0,0,0,.06); }
</style>
""", unsafe_allow_html=True)

# ======== CONSTANTES ========
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "dados_ferias.xlsx")

# ======== FUNÇÕES ========

def carregar_dados_persistidos():
    """Carrega os dados salvos em disco, se existirem."""
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_excel(DATA_FILE, sheet_name="Planilha1", header=1)
            df = df.dropna(axis=1, how='all')
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df.columns = df.columns.str.strip()
            df = df.dropna(how='all')
            data_cols = [c for c in df.columns if 'Data' in str(c) and 'Ini' in str(c)]
            if not data_cols:
                data_cols = [c for c in df.columns if 'gozo' in str(c).lower()]
            if not data_cols:
                data_cols = [c for c in df.columns if 'PROGRAMAÇÃO' in str(c)]
            if not data_cols:
                return None, None, None
            cd = data_cols[0]
            df[cd] = pd.to_datetime(df[cd], errors='coerce', dayfirst=True)
            df = df.dropna(subset=[cd]).copy()
            df["Competência"] = df[cd].dt.strftime("%m/%Y")
            return df, cd, None
        except Exception:
            return None, None, None
    return None, None, None

def salvar_dados_persistidos(df):
    """Salva o dataframe no arquivo persistente em disco."""
    os.makedirs(DATA_DIR, exist_ok=True)
    df_export = df.drop(columns=["Competência"], errors='ignore')
    with pd.ExcelWriter(DATA_FILE, engine='openpyxl') as w:
        df_export.to_excel(w, sheet_name="Planilha1", index=False, startrow=1)
        ws = w.sheets["Planilha1"]
        ws.cell(row=1, column=1, value="PROGRAMAÇÃO DE FÉRIAS")

def resetar_dados():
    """Remove o arquivo persistente e limpa a session_state."""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    for k in ["df_original", "df_trabalho", "competencia_sel", "uploaded_name", "gestor_sel", "empresa_sel", "coluna_data", "data_carregada"]:
        st.session_state[k] = None if k not in ["gestor_sel", "empresa_sel"] else []
    st.session_state["ano_sel"] = 2026
    st.session_state["todas"] = False

def processar_planilha(file):
    df = pd.read_excel(file, sheet_name="Planilha1", header=1)
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.columns = df.columns.str.strip()
    df = df.dropna(how='all')
    data_cols = [c for c in df.columns if 'PROGRAMAÇÃO' in str(c) and 'gozo' in str(c).lower()]
    if not data_cols: data_cols = [c for c in df.columns if 'gozo' in str(c).lower()]
    if not data_cols: data_cols = [c for c in df.columns if 'Data' in str(c) and 'Ini' in str(c)]
    if not data_cols: return None, None, "Coluna de data não encontrada"
    cd = data_cols[0]
    df[cd] = pd.to_datetime(df[cd], errors='coerce', dayfirst=True)
    df = df.dropna(subset=[cd]).copy()
    df["Competência"] = df[cd].dt.strftime("%m/%Y")
    return df, cd, None

def exibir_calendario(df):
    meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    comps = sorted(df["Competência"].unique())
    anos = sorted(set(int(c.split("/")[1]) for c in comps))
    st.sidebar.markdown("### 📅 Competência")
    c1,c2,c3 = st.sidebar.columns([1,2,1])
    with c1:
        if st.button("◀", key="ano_prev", use_container_width=True):
            i = anos.index(st.session_state["ano_sel"])
            if i > 0: st.session_state["ano_sel"] = anos[i-1]; st.rerun()
    with c2:
        st.markdown(f"<div style='text-align:center;font-weight:700;font-size:1rem;color:#0f172a;padding-top:8px'>{st.session_state['ano_sel']}</div>", unsafe_allow_html=True)
    with c3:
        if st.button("▶", key="ano_next", use_container_width=True):
            i = anos.index(st.session_state["ano_sel"])
            if i < len(anos)-1: st.session_state["ano_sel"] = anos[i+1]; st.rerun()

    # Todas
    todas_on = st.session_state.get("todas", False)
    if st.sidebar.button("📋 TODAS AS COMPETÊNCIAS", key="btn_todas", use_container_width=True, type="primary" if todas_on else "secondary"):
        st.session_state["todas"] = not st.session_state["todas"]; st.rerun()

    # Grid 3x4
    a = st.session_state["ano_sel"]
    for r in range(4):
        cols = st.sidebar.columns(3)
        for ci in range(3):
            m = r*3+ci+1
            comp = f"{m:02d}/{a}"
            with cols[ci]:
                ativo = (st.session_state.get("competencia_sel") == comp and not st.session_state.get("todas", False))
                if comp in comps:
                    if st.button(meses[m-1], key=f"mes_{m}", use_container_width=True, type="primary" if ativo else "secondary"):
                        st.session_state["competencia_sel"] = comp; st.session_state["todas"] = False; st.rerun()
                else:
                    st.button(meses[m-1], key=f"mes_{m}_d", use_container_width=True, disabled=True)

def verificar_alertas(df_d, cd, cq):
    hoje = datetime.now().date()
    alertas = []
    if cd not in df_d.columns or cq not in df_d.columns: return alertas
    for idx, row in df_d.iterrows():
        try:
            di = pd.to_datetime(row[cd]).date()
            q = int(float(row[cq]))
            dfim = di + timedelta(days=q-1)
            dret = di + timedelta(days=q)
            if hoje == dret - timedelta(days=1):
                nome = row.get("Empregado", str(idx))
                mat = row.get("Matrícula", row.get("Matricula", ""))
                if pd.isna(mat): mat = ""
                alertas.append({"nome": nome, "matricula": mat, "data_fim": dfim.strftime("%d/%m/%Y"), "data_retorno": dret.strftime("%d/%m/%Y")})
        except: continue
    return alertas

# ======== SESSION STATE ========
keys = ["df_original","df_trabalho","competencia_sel","ano_sel","todas","uploaded_name","gestor_sel","empresa_sel","coluna_data","data_carregada"]
defaults = [None, None, None, 2026, False, None, [], [], None, False]
for k, d in zip(keys, defaults):
    if k not in st.session_state:
        st.session_state[k] = d

# ======== CARREGAMENTO AUTOMÁTICO DOS DADOS PERSISTIDOS ========
if not st.session_state.get("data_carregada", False) and st.session_state["df_original"] is None:
    df_persist, cd_persist, err_persist = carregar_dados_persistidos()
    if df_persist is not None and cd_persist is not None:
        st.session_state["df_original"] = df_persist.copy()
        st.session_state["df_trabalho"] = df_persist.copy()
        st.session_state["coluna_data"] = cd_persist
        comps = sorted(df_persist["Competência"].unique())
        if comps:
            st.session_state["competencia_sel"] = comps[0]
    st.session_state["data_carregada"] = True

# ======== CABEÇALHO ========
st.title("🏖️ Dashboard de Programação de Férias 2026")
st.markdown('<p style="font-size:.8rem;color:#94a3b8">Visualize, edite e exporte as férias previstas por <strong>competência</strong>, gestor e empresa.</p>', unsafe_allow_html=True)

# ======== UPLOAD ========
uf = st.file_uploader("📂 Faça upload da planilha (.xlsx ou .xlsm)", type=["xlsx","xlsm"], key="fu")

if uf:
    if st.session_state.get("uploaded_name") != uf.name:
        st.session_state["uploaded_name"] = uf.name
        st.session_state["df_original"] = None; st.session_state["df_trabalho"] = None; st.session_state["competencia_sel"] = None

    if st.session_state["df_original"] is None:
        dfc, cd, err = processar_planilha(uf)
        if err: st.error(f"❌ {err}"); st.stop()
        st.session_state["df_original"] = dfc.copy()
        st.session_state["df_trabalho"] = dfc.copy()
        st.session_state["coluna_data"] = cd
        # Salva automaticamente em disco
        salvar_dados_persistidos(dfc)
        comps = sorted(dfc["Competência"].unique())
        if comps: st.session_state["competencia_sel"] = comps[0]
        st.rerun()

if st.session_state["df_trabalho"] is not None:
    dfo = st.session_state["df_original"]
    dft = st.session_state["df_trabalho"]
    cd = st.session_state["coluna_data"]

    # ======== SIDEBAR ========
    with st.sidebar:
        st.markdown("### 🏖️ Férias 2026"); st.markdown("---")
        exibir_calendario(dft)
        st.markdown("---")
        st.markdown("### 👤 Gestor(es)")
        if "Gestor" in dft.columns:
            gs = sorted(dft["Gestor"].dropna().unique())
            gsel = st.multiselect("Gestores", gs, default=st.session_state.get("gestor_sel", gs), label_visibility="collapsed", key="gms")
            st.session_state["gestor_sel"] = gsel
        else: gsel = None
        st.markdown("### 🏢 Empresa(s)")
        if "Empresa" in dft.columns:
            es = sorted(dft["Empresa"].dropna().unique())
            esel = st.multiselect("Empresas", es, default=st.session_state.get("empresa_sel", es), label_visibility="collapsed", key="ems")
            st.session_state["empresa_sel"] = esel
        else: esel = None

        # ======== BOTÃO RESETAR ========
        st.markdown("---")
        if st.button("🔄 Resetar Dados", type="secondary", use_container_width=True, help="Apaga todos os dados salvos e permite fazer upload de uma nova planilha."):
            resetar_dados()
            st.rerun()

        if os.path.exists(DATA_FILE):
            st.caption(f"💾 Dados salvos em {datetime.fromtimestamp(os.path.getmtime(DATA_FILE)).strftime('%d/%m/%Y %H:%M')}")

    # ======== FILTROS ========
    dff = dft.copy()
    todas = st.session_state.get("todas", False)
    if todas: titulo = "TODAS AS COMPETÊNCIAS"
    else:
        cs = st.session_state.get("competencia_sel")
        if cs: dff = dff[dff["Competência"] == cs]; titulo = cs
        else: titulo = "Selecione uma competência"
    if gsel and "Gestor" in dff.columns: dff = dff[dff["Gestor"].isin(gsel)]
    if esel and "Empresa" in dff.columns: dff = dff[dff["Empresa"].isin(esel)]

    # ======== MÉTRICAS ========
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("👥 Colaboradores", len(dff), delta=f"de {len(dfo)} total")
    with c2:
        cq = None
        for cn in ["QTD Dias","Dias direito","Dias gozados"]:
            if cn in dff.columns: cq = cn; break
        if cq:
            dv = pd.to_numeric(dff[cq], errors='coerce').sum()
            st.metric("📆 Dias Totais", f"{dv:.0f}")
        else: st.metric("📆 Dias Totais", "N/A")
    with c3:
        if "Gestor" in dff.columns: st.metric("👤 Gestores", dff["Gestor"].nunique())
    with c4:
        if "Empresa" in dff.columns: st.metric("🏢 Empresas", dff["Empresa"].nunique())

    # ======== ALERTAS ========
    cq_final = None
    for cn in ["QTD Dias","Dias direito","Dias gozados"]:
        if cn in dff.columns: cq_final = cn; break
    if cd and cq_final:
        alertas = verificar_alertas(dff, cd, cq_final)
        if alertas:
            st.warning("🔓 **Atenção: Solicitações de Desbloqueio Pendentes**")
            for a in alertas:
                st.info(f"🔑 **{a['nome']}** (Matrícula: {a['matricula']}) — Férias terminam em **{a['data_fim']}**. Retorno em **{a['data_retorno']}**. **Solicitar desbloqueio!**")

    # ======== TABELA EDITÁVEL ========
    st.subheader(f"📋 Colaboradores — {titulo}")
    st.caption(f"{len(dff)} registros encontrados")

    if len(dff) > 0:
        cols_disp = [c for c in dff.columns if c != "Competência"]
        df_disp = dff[cols_disp].copy()
        col_dt = []
        for c in df_disp.columns:
            if pd.api.types.is_datetime64_any_dtype(df_disp[c]):
                df_disp[c] = df_disp[c].dt.strftime("%d/%m/%Y")
                col_dt.append(c)

        edited = st.data_editor(df_disp, use_container_width=True, num_rows="fixed", hide_index=True, key="de", height=450)

        # Detecta alterações
        df_disp_orig = dff[cols_disp].copy()
        for c in df_disp_orig.columns:
            if pd.api.types.is_datetime64_any_dtype(df_disp_orig[c]):
                df_disp_orig[c] = df_disp_orig[c].dt.strftime("%d/%m/%Y")

        alteracoes = {}
        for c in edited.columns:
            if c in df_disp_orig.columns:
                mask = edited[c] != df_disp_orig[c]
                if mask.any():
                    for idx in edited.index[mask]:
                        if idx not in alteracoes: alteracoes[idx] = {}
                        alteracoes[idx][c] = edited.loc[idx, c]

        if alteracoes:
            nc = sum(len(v) for v in alteracoes.values())
            ca, ci = st.columns([1,3])
            with ca:
                if st.button(f"💾 Aplicar {nc} alteração(ões)", type="primary", use_container_width=True):
                    dft_up = dft.copy()
                    for idx_d, mud in alteracoes.items():
                        idx_o = dff.index[idx_d]
                        for col, nv in mud.items():
                            if col in col_dt or any(x in col.lower() for x in ['data','início','inicio','fim','limite','admissão','admissao','gozo','aquisitivo']):
                                try: dft_up.loc[idx_o, col] = pd.to_datetime(nv, dayfirst=True)
                                except: dft_up.loc[idx_o, col] = nv
                            else:
                                vo = dft.loc[idx_o, col]
                                if pd.api.types.is_numeric_dtype(type(vo)):
                                    try: dft_up.loc[idx_o, col] = float(str(nv).replace(',','.'))
                                    except: dft_up.loc[idx_o, col] = nv
                                else: dft_up.loc[idx_o, col] = nv
                        # Recalcula data retorno
                        if cd in mud or cq_final in mud:
                            try:
                                di = pd.to_datetime(dft_up.loc[idx_o, cd])
                                qd = int(float(dft_up.loc[idx_o, cq_final]))
                                for cc in dft_up.columns:
                                    if 'fim' in cc.lower(): dft_up.loc[idx_o, cc] = di + timedelta(days=qd-1)
                                    elif 'retorno' in cc.lower(): dft_up.loc[idx_o, cc] = di + timedelta(days=qd)
                            except: pass
                    if cd in [x for ml in alteracoes.values() for x in ml]:
                        dft_up["Competência"] = dft_up[cd].dt.strftime("%m/%Y")
                    st.session_state["df_trabalho"] = dft_up
                    # Salva automaticamente após aplicar alterações
                    salvar_dados_persistidos(dft_up)
                    st.success(f"✅ {nc} alteração(ões) aplicada(s) e salva(s)!"); st.rerun()
            with ci: st.info(f"🟡 {nc} célula(s) modificada(s). Clique em 'Aplicar' para salvar.")

        # ======== DOWNLOAD ========
        st.markdown("---"); st.subheader("💾 Exportar Dados")
        dl1, dl2 = st.columns(2)
        with dl1:
            output = BytesIO()
            df_exp = dft.drop(columns=["Competência"], errors='ignore')
            df_exp_f = df_exp.copy()
            if not todas and st.session_state.get("competencia_sel"):
                df_exp_f = df_exp_f[df_exp_f[cd].dt.strftime("%m/%Y") == st.session_state["competencia_sel"]]
            if gsel and "Gestor" in df_exp_f.columns: df_exp_f = df_exp_f[df_exp_f["Gestor"].isin(gsel)]
            if esel and "Empresa" in df_exp_f.columns: df_exp_f = df_exp_f[df_exp_f["Empresa"].isin(esel)]
            with pd.ExcelWriter(output, engine='openpyxl') as w:
                df_exp_f.to_excel(w, sheet_name="Planilha1", index=False, startrow=1)
                ws = w.sheets["Planilha1"]
                ws.cell(row=1, column=1, value=f"PROGRAMAÇÃO DE FÉRIAS {st.session_state.get('ano_sel',2026)}")
            output.seek(0)
            st.download_button("📥 Baixar Planilha (.xlsx)", data=output,
                file_name=f"ferias_{titulo.replace('/','_').replace(' ','_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        with dl2:
            csv = df_disp.to_csv(index=False, encoding='utf-8-sig')
            st.download_button("📥 Baixar CSV", data=csv,
                file_name=f"ferias_{titulo.replace('/','_').replace(' ','_')}.csv",
                mime="text/csv", use_container_width=True)

    else:
        st.info("Nenhum colaborador encontrado para os filtros selecionados.")

    with st.expander("ℹ️ Informações sobre os dados"):
        st.write(f"""
        - **Total de registros:** {len(dfo)}
        - **Período:** {dfo[cd].min().strftime('%m/%Y')} a {dfo[cd].max().strftime('%m/%Y')}
        - **Colunas:** {len(dfo.columns)}
        - **Competências disponíveis:** {dfo['Competência'].nunique()}
        """)

else:
    if os.path.exists(DATA_FILE):
        st.info("📂 Dados salvos encontrados. Carregando automaticamente...")
        st.stop()
    else:
        st.info("⬆️ Faça o upload da planilha para visualizar o dashboard.")
        st.markdown("""
        ### 📋 Funcionalidades:
        ✅ Upload de .xlsx/.xlsm  
        ✅ **Persistência automática** — dados ficam salvos no portal  
        ✅ Calendário de competências com opção "Todas"  
        ✅ Filtro por gestor e empresa  
        ✅ **Edição célula a célula de TODOS os campos**  
        ✅ **Cálculo automático de Data Retorno**  
        ✅ **Alerta de desbloqueio (1 dia antes)**  
        ✅ **Download da planilha original atualizada**  
        ✅ Botão **Resetar Dados** para subir nova planilha  
        """)