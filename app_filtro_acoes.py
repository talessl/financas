import streamlit as st
import pandas as pd
import yfinance as yf
import indices
import acoesB3
import time

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Hub de Filtros B3",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
    .main {background-color: #0e1117;}
    div[data-testid="stMetricValue"] {font-size: 24px;}
</style>
""", unsafe_allow_html=True)

st.title("📈 Hub de Estratégias B3")
st.markdown("**Selecione um dos seus scripts de filtragem para executar.**")
st.divider()

# ==========================================
# LÓGICA DOS FILTROS
# ==========================================

def executar_filtro_1(tickers):
    """Lógica baseada no filtro1.py (Sobrevenda)"""
    st.info("📉 Executando Filtro 1: Buscando oportunidades de Sobrevenda (RSI < 30 e Stoch < 20)...")
    
    status_text = st.empty()
    bar = st.progress(0)
    
    resultados_rsi = []
    resultados_stoch = []
    
    status_text.text("Baixando dados de mercado...")
    dados_todos = yf.download(tickers=tickers, period="3mo", progress=False, group_by='ticker')
    
    total = len(tickers)
    
    for i, ticker in enumerate(tickers):
        bar.progress((i + 1) / total)
        try:
            if len(tickers) == 1: dados = dados_todos
            else: dados = dados_todos[ticker]
            
            # Limpeza básica
            dados = dados.dropna()
            if dados.empty: continue

            metodo = indices.Indices(dados)
            
            # 1. RSI
            metodo.rsi()
            ultimo_rsi = metodo.dados['RSI_14'].iloc[-1]
            preco = metodo.dados['Close'].iloc[-1]
            
            if ultimo_rsi < 30:
                resultados_rsi.append(ticker)
            
            # 2. Stochastic
            metodo.stoch()
            k = metodo.dados['STOCHk_14_3_3'].iloc[-1]
            d = metodo.dados['STOCHd_14_3_3'].iloc[-1]
            
            if k < 20 and d < 20:
                resultados_stoch.append({'Ticker': ticker, 'Preço': preco, 'Stoch K': k, 'Stoch D': d, 'RSI': ultimo_rsi})
                
        except Exception:
            pass
            
    bar.empty()
    status_text.empty()
    
    tickers_rsi = set(resultados_rsi)
    df_final = pd.DataFrame([x for x in resultados_stoch if x['Ticker'] in tickers_rsi])
    
    return df_final

def executar_filtro_2(tickers):
    """Lógica baseada no filtro2.py (Agressivo Sem Liquidez)"""
    st.info("⚡ Executando Filtro 2: Análise Técnica Agressiva (Sem filtro de liquidez)...")
    
    status_text = st.empty()
    status_text.text("Baixando dados (6 meses)...")
    
    dados_todos = yf.download(tickers=tickers, period="6mo", progress=True, group_by='ticker')
    
    resultados = {'didi': [], 'adx': [], 'rsi': [], 'stoch': [], 'trix': []}
    detalhes = []
    
    total = len(tickers)
    bar = st.progress(0)
    
    for i, ticker in enumerate(tickers):
        bar.progress((i + 1) / total)
        try:
            if len(tickers) == 1: dados = dados_todos
            else: dados = dados_todos[ticker]
            
            if dados['Close'].isna().all(): continue

            metodo = indices.Indices(dados)
            metodo.didi()
            metodo.pfr()
            metodo.adx()
            metodo.rsi()
            metodo.stoch()
            metodo.trix()
            
            preco = metodo.dados['Close'].iloc[-1]
            sinais = 0
            
            # DIDI
            sma3 = metodo.dados['SMA_3'].iloc[-1]
            sma8 = metodo.dados['SMA_8'].iloc[-1]
            sma20 = metodo.dados['SMA_20'].iloc[-1]
            sma72 = metodo.dados['SMA_72'].iloc[-1]
            if sma3 > sma8 > sma20 and preco > sma72:
                resultados['didi'].append(ticker); sinais += 1
            
            # ADX
            if metodo.dados['ADX_14'].iloc[-1] > 25 and metodo.dados['DMP_14'].iloc[-1] > metodo.dados['DMN_14'].iloc[-1]:
                resultados['adx'].append(ticker); sinais += 1
                
            # RSI
            if 40 < metodo.dados['RSI_14'].iloc[-1] < 70:
                resultados['rsi'].append(ticker); sinais += 1
                
            # STOCH
            k, d = metodo.dados['STOCHk_14_3_3'].iloc[-1], metodo.dados['STOCHd_14_3_3'].iloc[-1]
            kp, dp = metodo.dados['STOCHk_14_3_3'].iloc[-2], metodo.dados['STOCHd_14_3_3'].iloc[-2]
            if (kp <= dp) and (k > d) and k < 80:
                resultados['stoch'].append(ticker); sinais += 1
                
            # TRIX
            trix = metodo.dados['TRIX_30_9'].iloc[-1]
            trix_ant = metodo.dados['TRIX_30_9'].iloc[-2]
            if trix > 0 or (trix_ant < 0 and trix > trix_ant):
                resultados['trix'].append(ticker); sinais += 1
            
            if sinais >= 4:
                detalhes.append({'Ticker': ticker, 'Preço': preco, 'Sinais': sinais})
                
        except Exception:
            pass
            
    bar.empty()
    status_text.empty()
    return pd.DataFrame(detalhes), resultados

def executar_filtro_3(tickers, volume_minimo):
    """Lógica baseada no filtro3.py (Agressivo + Liquidez)"""
    st.info(f"💧 Executando Filtro 3: Técnica Agressiva + Liquidez (Vol min: {volume_minimo})...")
    
    status_text = st.empty()
    status_text.text("Baixando dados e analisando liquidez...")
    
    dados_todos = yf.download(tickers=tickers, period="6mo", progress=True, group_by='ticker')
    
    detalhes = []
    rejeitadas = []
    
    bar = st.progress(0)
    total = len(tickers)
    dias_analise = 20 
    
    for i, ticker in enumerate(tickers):
        bar.progress((i + 1) / total)
        try:
            if len(tickers) == 1: dados = dados_todos
            else: dados = dados_todos[ticker]
            
            # Verificação básica de dados vazios
            if dados is None or dados.empty: continue
            if 'Close' not in dados.columns: continue
            if dados['Close'].isna().all(): continue
            
            # ============================================
            # 1. FILTRO DE LIQUIDEZ
            # ============================================
            vol_medio = dados['Volume'].tail(dias_analise).mean()
            dias_sem_vol = (dados['Volume'].tail(dias_analise) == 0).sum()
            
            # Evitar divisão por zero se média for 0 ou nula
            mean_close = dados['Close'].tail(dias_analise).mean()
            if mean_close == 0 or pd.isna(mean_close):
                volatilidade = 0
            else:
                volatilidade = dados['Close'].tail(dias_analise).std() / mean_close
                
            spread = ((dados['High'] - dados['Low']) / dados['Close']).tail(dias_analise).mean()
            
            tem_liquidez = (
                vol_medio >= volume_minimo and
                ((dias_sem_vol / dias_analise) * 100) < 20 and
                volatilidade > 0.01 and
                spread > 0.005
            )
            
            if not tem_liquidez:
                rejeitadas.append({'Ticker': ticker, 'Motivo': 'Baixa Liquidez', 'Volume Médio': f"{vol_medio:,.0f}"})
                continue

            # ============================================
            # 2. ANÁLISE TÉCNICA
            # ============================================
            metodo = indices.Indices(dados)
            
            # IMPORTANTE: A ordem e a presença dos métodos deve ser igual ao script original
            metodo.didi()
            metodo.pfr()  # Adicionado de volta para manter consistência interna da classe
            metodo.adx()
            metodo.rsi()
            metodo.stoch()
            metodo.trix()
            
            preco = metodo.dados['Close'].iloc[-1]
            sinais = 0
            
            # DIDI
            sma3 = metodo.dados['SMA_3'].iloc[-1]
            sma8 = metodo.dados['SMA_8'].iloc[-1]
            sma20 = metodo.dados['SMA_20'].iloc[-1]
            sma72 = metodo.dados['SMA_72'].iloc[-1]
            
            if sma3 > sma8 > sma20 and preco > sma72: sinais += 1
            
            # ADX
            adx = metodo.dados['ADX_14'].iloc[-1]
            dmp = metodo.dados['DMP_14'].iloc[-1]
            dmn = metodo.dados['DMN_14'].iloc[-1]
            
            if adx > 25 and dmp > dmn: sinais += 1
            
            # RSI
            if 40 < metodo.dados['RSI_14'].iloc[-1] < 70: sinais += 1
            
            # STOCH
            k = metodo.dados['STOCHk_14_3_3'].iloc[-1]
            d = metodo.dados['STOCHd_14_3_3'].iloc[-1]
            kp = metodo.dados['STOCHk_14_3_3'].iloc[-2]
            dp = metodo.dados['STOCHd_14_3_3'].iloc[-2]
            
            if (kp <= dp) and (k > d) and k < 80: sinais += 1
            
            # TRIX
            trix = metodo.dados['TRIX_30_9'].iloc[-1]
            trix_a = metodo.dados['TRIX_30_9'].iloc[-2]
            
            if trix > 0 or (trix_a < 0 and trix > trix_a): sinais += 1
            
            if sinais >= 4:
                detalhes.append({
                    'Ticker': ticker, 
                    'Preço': preco, 
                    'Sinais': sinais, 
                    'Volume Médio': f"{vol_medio:,.0f}"
                })
                
        except Exception as e:
            # Imprime erro no terminal para debug, mas não para o app
            print(f"Erro ao processar {ticker}: {e}")
            pass
            
    bar.empty()
    status_text.empty()
    return pd.DataFrame(detalhes), pd.DataFrame(rejeitadas)

# ==========================================
# SIDEBAR - SELEÇÃO
# ==========================================
with st.sidebar:
    st.header("⚙️ Configurações")
    
    escolha = st.radio(
        "Qual script você quer rodar?",
        [
            "Filtro 1 (Sobrevenda RSI+Stoch)", 
            "Filtro 2 (Técnico Agressivo)", 
            "Filtro 3 (Técnico + Liquidez)"
        ],
        index=2
    )
    
    vol_input = 100000
    if "Filtro 3" in escolha:
        st.info("ℹ️ Parâmetro exclusivo do Filtro 3")
        vol_input = st.number_input("Volume Mínimo Diário", value=100000, step=50000)

    st.divider()
    executar = st.button("🚀 EXECUTAR ANÁLISE", type="primary", use_container_width=True)

# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================
if executar:
    with st.spinner("Carregando lista de ações baratas (acoesB3)..."):
        tickers = acoesB3.acoes_baratas()
    
    st.write(f"🔎 Analisando **{len(tickers)}** ativos com a estratégia: **{escolha}**")
    
    start_time = time.time()
    
    if "Filtro 1" in escolha:
        df_res = executar_filtro_1(tickers)
        if not df_res.empty:
            st.success(f"✅ Encontradas {len(df_res)} ações em Sobrevenda!")
            st.dataframe(df_res, use_container_width=True)
        else:
            st.warning("Nenhuma ação atendeu aos critérios.")
            
    elif "Filtro 2" in escolha:
        df_res, stats = executar_filtro_2(tickers)
        if not df_res.empty:
            st.success(f"✅ Encontradas {len(df_res)} ações com 4+ Sinais!")
            col1, col2 = st.columns([2, 1])
            with col1:
                st.dataframe(df_res.sort_values('Sinais', ascending=False), use_container_width=True)
            with col2:
                st.write("📊 **Sinais:**")
                st.write(f"- Didi: {len(stats['didi'])}")
                st.write(f"- ADX: {len(stats['adx'])}")
                st.write(f"- TRIX: {len(stats['trix'])}")
        else:
            st.warning("Nenhuma ação atingiu 4 sinais.")

    elif "Filtro 3" in escolha:
        df_res, df_rej = executar_filtro_3(tickers, vol_input)
        if not df_res.empty:
            st.success(f"✅ Encontradas {len(df_res)} ações (Técnica + Liquidez)!")
            st.dataframe(df_res.sort_values('Sinais', ascending=False), use_container_width=True)
        else:
            st.warning("Nenhuma ação aprovada.")
            
        with st.expander("🗑️ Ver ações rejeitadas por falta de liquidez"):
            st.dataframe(df_rej, use_container_width=True)

    tempo = time.time() - start_time
    st.caption(f"Tempo de execução: {tempo:.2f} segundos")

else:
    st.info("👈 Selecione o filtro desejado na barra lateral e clique em EXECUTAR.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 1️⃣ Filtro 1")
        st.markdown("RSI < 30 e Stochastic < 20.")
    with col2:
        st.markdown("### 2️⃣ Filtro 2")
        st.markdown("Técnico Agressivo (Sem Liquidez).")
    with col3:
        st.markdown("### 3️⃣ Filtro 3")
        st.markdown("Técnico Agressivo + Filtro de Liquidez.")