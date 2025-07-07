# Arquivo: main.py (Versão Corrigida e Final)
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import indices

# ===================================================================
# 1. CONFIGURAÇÃO
# ===================================================================

# --- Defina aqui a lista de ações que você quer analisar ---
LISTA_DE_ACOES = ['AVLL3.SA', 'AZEV4.SA', 'AZUL4.SA', 'CEED3.SA', 'MGEL4.SA', 'RCSL3.SA', 'RDNI3.SA', 'RNEW11.SA', 'RNEW3.SA', 'RNEW4.SA', 'SEQL3.SA', 'SNSY5.SA', 'TRIS3.SA', 'WHRL4.SA']

LIMITE = 2

DATA_INICIO = "2025-01-01"
TICKER_PARA_VALIDAR = LISTA_DE_ACOES[0] # Valida a primeira ação da lista

# ===================================================================
# 2. FUNÇÃO DE ANÁLISE (COM LÓGICA CORRIGIDA)
# ===================================================================

# Em main.py, substitua a função de análise por esta versão:

def analisar_sinais_para_acao(ticker, limite_de_sinais=4, dias_para_verificar=3):
    """
    Analisa um ticker, imprime um detalhamento dos indicadores que pontuaram,
    e retorna um resumo do sinal.
    """
    print(f"--- Analisando {ticker}... ---")
    try:
        dados = yf.download(ticker, start=DATA_INICIO, progress=False)
        if dados.empty: return "Dados Insuficientes", None
        
        # Garante que as colunas não sejam MultiIndex
        if isinstance(dados.columns, pd.MultiIndex):
            dados.columns = dados.columns.droplevel(1)
        
        acao = indices.Indices(dataframe_acao=dados)
        acao.calcular_todos()
        df = acao.dados
        
        # --- Lógica de Condições e Score ---
        cond_adx_compra = (df['ADX_14'] > 22) & (df['DMP_14'] > df['DMN_14'])
        cond_didi_compra = (df['SMA_3'].shift(1) < df['SMA_8'].shift(1)) & (df['SMA_3'] > df['SMA_8'])
        cond_trix_compra = (df['TRIX_30_9'].shift(1) < 0) & (df['TRIX_30_9'] > 0)
        cond_stoch_compra = (df['STOCHk_14_3_3'].shift(1) < df['STOCHd_14_3_3'].shift(1)) & \
                              (df['STOCHk_14_3_3'] > df['STOCHd_14_3_3'])
        cond_rsi_compra = df['RSI_14'] < 55

        condicoes_compra = {
            "ADX (Força + Direção de Alta)": cond_adx_compra,
            "DIDI (Cruzamento de Compra)": cond_didi_compra,
            "TRIX (Cruzamento p/ Cima)": cond_trix_compra,
            "Estocástico (Cruzamento de Compra)": cond_stoch_compra,
            "RSI (Não Sobrecomprado)": cond_rsi_compra
        }

        # <<< CORREÇÃO 1: Usando o dicionário para calcular o score >>>
        df['score_compra'] = sum(cond.astype(int) for cond in condicoes_compra.values())

        cond_adx_venda = (df['ADX_14'] > 25) & (df['DMN_14'] > df['DMP_14'])
        cond_didi_venda = ((df['SMA_3'].shift(1) > df['SMA_8'].shift(1)) & (df['SMA_3'] < df['SMA_8'])) & \
                          ((df['SMA_3'].shift(1) > df['SMA_20'].shift(1)) & (df['SMA_3'] < df['SMA_20']))
        cond_trix_venda = (df['TRIX_30_9'].shift(1) > 0) & (df['TRIX_30_9'] < 0)
        cond_stoch_venda = (df['STOCHk_14_3_3'].shift(1) > df['STOCHd_14_3_3'].shift(1)) & \
                           (df['STOCHk_14_3_3'] < df['STOCHd_14_3_3']) & (df['STOCHk_14_3_3'] > 70)
        cond_rsi_venda = df['RSI_14'] > 60

        condicoes_venda = {
            "ADX (Força + Direção de Baixa)": cond_adx_venda,
            "DIDI (Agulhada de Venda)": cond_didi_venda,
            "TRIX (Cruzamento p/ Baixo)": cond_trix_venda,
            "Estocástico (Cruzamento de Venda em Sobrecompra)": cond_stoch_venda,
            "RSI (Sobrecomprado)": cond_rsi_venda
        }
        
        # <<< CORREÇÃO 1: Usando o dicionário para calcular o score >>>
        df['score_venda'] = sum(cond.astype(int) for cond in condicoes_venda.values())
        
        # --- Lógica de Verificação e Impressão de Detalhes ---
        status_final = "Sem Sinal Relevante"
        df_recente = df.tail(dias_para_verificar)
        
        # Verifica Sinais de Compra
        dias_sinal_compra = df_recente[df_recente['score_compra'] >= limite_de_sinais]
        if not dias_sinal_compra.empty:
            score_hoje = df.iloc[-1]['score_compra']
            status_final = f"COMPRA ({len(dias_sinal_compra)} sinal/sinais nos últimos {dias_para_verificar} dias. Score hoje: {score_hoje:.0f})"
            
            print(f"  -> DETALHE DO SINAL DE COMPRA para {ticker}:")
            for data, linha in dias_sinal_compra.iterrows():
                # <<< CORREÇÃO 2: Verificando o valor diretamente na condição >>>
                indicadores_ativos = [nome for nome, cond in condicoes_compra.items() if cond.loc[data]]
                print(f"     - Em {data.date()}: Score {linha['score_compra']:.0f} -> ({', '.join(indicadores_ativos)})")

        # Verifica Sinais de Venda
        dias_sinal_venda = df_recente[df_recente['score_venda'] >= limite_de_sinais]
        if not dias_sinal_venda.empty:
            score_hoje = df.iloc[-1]['score_venda']
            status_final = f"VENDA ({len(dias_sinal_venda)} sinal/sinais nos últimos {dias_para_verificar} dias. Score hoje: {score_hoje:.0f})"

            print(f"  -> DETALHE DO SINAL DE VENDA para {ticker}:")
            for data, linha in dias_sinal_venda.iterrows():
                # <<< CORREÇÃO 2: Verificando o valor diretamente na condição >>>
                indicadores_ativos = [nome for nome, cond in condicoes_venda.items() if cond.loc[data]]
                print(f"     - Em {data.date()}: Score {linha['score_venda']:.0f} -> ({', '.join(indicadores_ativos)})")
                
        return status_final, df

    except Exception as e:
        print(f"ERRO ao analisar {ticker}: {e}")
        return "Erro na Análise", None

# ===================================================================
# 3. EXECUÇÃO PRINCIPAL E RESUMO
# ===================================================================
# (Esta parte do código não precisa de alterações)
if __name__ == "__main__":
    resumo_sinais = {}
    dados_processados = {}
    for ticker in LISTA_DE_ACOES:
        resultado, df_processado = analisar_sinais_para_acao(ticker, limite_de_sinais=LIMITE)
        resumo_sinais[ticker] = resultado
        if df_processado is not None:
            dados_processados[ticker] = df_processado
    print("\n\n" + "="*50)
    print("           RESUMO FINAL DO SCANNER DE MERCADO")
    print(f"           Análise do dia: {pd.Timestamp.today().date()}")
    print("="*50)
    houve_sinal = False
    for ticker, status in resumo_sinais.items():
        if status != "Sem Sinal Ideal" and status != "Dados Insuficientes" and status != "Erro na Análise":
            print(f"ATIVO: {ticker:<10} | SINAL: {status}")
            houve_sinal = True
    if not houve_sinal:
        print("Nenhum ativo na lista apresentou um sinal ideal hoje.")
    print("="*50)

# ===================================================================
# 4. ETAPA DE VALIDAÇÃO VISUAL (COM NOMES CORRIGIDOS)
# ===================================================================
print(f"\n--- VALIDAÇÃO VISUAL PARA: {TICKER_PARA_VALIDAR} ---")
if TICKER_PARA_VALIDAR in dados_processados:
    df_validacao = dados_processados[TICKER_PARA_VALIDAR]
    print("\nÚltimos 10 dias de dados e indicadores calculados:")
    # CORREÇÃO: Nomes de colunas exatos gerados pelo pandas-ta
    colunas_para_ver = ['Close', 'RSI_14', 'STOCHk_14_3_3', 'STOCHd_14_3_3', 'TRIX_30_9', 'TRIXs_30_9', 'ADX_14']
    print(df_validacao[colunas_para_ver].tail(10))

    print("\nGerando gráfico de validação...")
    dados_para_plotar = df_validacao.tail(180)
    
    # CORREÇÃO: Usando as colunas de sinal corretas para Stoch e TRIX
    paineis_adicionais = [
        mpf.make_addplot(dados_para_plotar[['SMA_3', 'SMA_8', 'SMA_20']], panel=0),
        mpf.make_addplot(dados_para_plotar['RSI_14'], panel=2, ylabel='RSI'),
        # Plotando a linha K (azul) e a linha D (laranja)
        mpf.make_addplot(dados_para_plotar['STOCHk_14_3_3'], panel=3, color='blue', ylabel='Estocástico'),
        mpf.make_addplot(dados_para_plotar['STOCHd_14_3_3'], panel=3, color='orange'),
        # Plotando a linha TRIX (verde) e sua linha de sinal (vermelha)
        mpf.make_addplot(dados_para_plotar['TRIX_30_9'], panel=4, color='green', ylabel='TRIX'),
        mpf.make_addplot(dados_para_plotar['TRIXs_30_9'], panel=4, color='red')
    ]

    mpf.plot(dados_para_plotar, 
             type='candle', 
             style='yahoo',
             title=f'{TICKER_PARA_VALIDAR} - Gráfico de Validação',
             ylabel='Preço (R$)',
             volume=True, 
             addplot=paineis_adicionais,
             figscale=1.5,
             panel_ratios=(6, 2, 2, 2, 2))
else:
    print(f"Não foi possível gerar a validação. Dados para {TICKER_PARA_VALIDAR} não foram processados ou continham erros.")