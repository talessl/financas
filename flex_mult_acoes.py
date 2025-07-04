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
LISTA_DE_ACOES = ['AALR3.SA', 'AVLL3.SA', 'AZEV4.SA', 'AZUL4.SA', 'BHIA3.SA', 'CEED3.SA', 'CRPG5.SA', 'GFSA3.SA', 'GSHP3.SA', 'MGEL4.SA', 'RCSL3.SA', 'RDNI3.SA', 'RNEW11.SA', 'RNEW3.SA', 'RNEW4.SA', 'SMTO3.SA', 'SNSY5.SA']

LIMITE = 2

DATA_INICIO = "2023-01-01"
TICKER_PARA_VALIDAR = LISTA_DE_ACOES[0] # Valida a primeira ação da lista

# ===================================================================
# 2. FUNÇÃO DE ANÁLISE (COM LÓGICA CORRIGIDA)
# ===================================================================

# Em main.py, substitua a função de análise por esta versão:

def analisar_sinais_para_acao(ticker, limite_de_sinais=4, dias_para_verificar=3):
    """
    Analisa um ticker usando um sistema de pontuação e verifica os últimos X dias.
    'limite_de_sinais': número mínimo de condições para um dia ser considerado um "sinal".
    'dias_para_verificar': a janela de tempo recente que nos interessa (ex: 3 dias).
    """
    print(f"--- Analisando {ticker}... ---")
    try:
        dados = yf.download(ticker, start=DATA_INICIO, progress=False)
        if dados.empty: return "Dados Insuficientes", None
        
        dados.columns = dados.columns.droplevel(1)
        
        acao = indices.Indices(dataframe_acao=dados)
        acao.calcular_todos()
        df = acao.dados
        
        # --- Lógica de Condições e Score ---
        # --- LÓGICA DE CONDIÇÕES MAIS FLEXÍVEL ---
        # ADX: Uma tendência "suficiente" já pode começar com ADX acima de 22
        cond_adx_compra = (df['ADX_14'] > 22) & (df['DMP_14'] > df['DMN_14'])

        # DIDI: Talvez a "agulhada" completa seja rara. Que tal apenas o cruzamento da média rápida com a intermediária?
        cond_didi_compra = (df['SMA_3'].shift(1) < df['SMA_8'].shift(1)) & (df['SMA_3'] > df['SMA_8'])

        # TRIX: O cruzamento do zero continua sendo um bom sinal
        cond_trix_compra = (df['TRIX_30_9'].shift(1) < 0) & (df['TRIX_30_9'] > 0)

        # ESTOCÁSTICO: Podemos exigir apenas o cruzamento, sem que ele precise estar na zona de sobrevenda
        cond_stoch_compra = (df['STOCHk_14_3_3'].shift(1) < df['STOCHd_14_3_3'].shift(1)) & \
                            (df['STOCHk_14_3_3'] > df['STOCHd_14_3_3'])

        # RSI: Em vez de < 40, podemos aceitar qualquer valor que não esteja sobrecomprado (ex: < 55)
        cond_rsi_compra = df['RSI_14'] < 55

        # O sistema de Score continua o mesmo, mas agora com condições mais fáceis de serem atingidas
        df['score_compra'] = (cond_adx_compra.astype(int) + cond_didi_compra.astype(int) + 
                            cond_trix_compra.astype(int) + cond_stoch_compra.astype(int) + 
                            cond_rsi_compra.astype(int))

        cond_adx_venda = (df['ADX_14'] > 25) & (df['DMN_14'] > df['DMP_14'])
        cond_didi_venda = ((df['SMA_3'].shift(1) > df['SMA_8'].shift(1)) & (df['SMA_3'] < df['SMA_8'])) & \
                          ((df['SMA_3'].shift(1) > df['SMA_20'].shift(1)) & (df['SMA_3'] < df['SMA_20']))
        cond_trix_venda = (df['TRIX_30_9'].shift(1) > 0) & (df['TRIX_30_9'] < 0)
        cond_stoch_venda = (df['STOCHk_14_3_3'].shift(1) > df['STOCHd_14_3_3'].shift(1)) & \
                           (df['STOCHk_14_3_3'] < df['STOCHd_14_3_3']) & (df['STOCHk_14_3_3'] > 70)
        cond_rsi_venda = df['RSI_14'] > 60
        
        df['score_venda'] = (cond_adx_venda.astype(int) + cond_didi_venda.astype(int) + 
                             cond_trix_venda.astype(int) + cond_stoch_venda.astype(int) + 
                             cond_rsi_venda.astype(int))
        
        # --- LÓGICA DE VERIFICAÇÃO FINAL MODIFICADA ---
        status_final = "Sem Sinal Relevante"
        
        # Pegamos apenas os últimos dias para análise
        df_recente = df.tail(dias_para_verificar)
        
        # Contamos quantos dias nos últimos X dias tiveram um score alto
        contagem_compra = (df_recente['score_compra'] >= limite_de_sinais).sum()
        contagem_venda = (df_recente['score_venda'] >= limite_de_sinais).sum()

        if contagem_compra > 0:
            # Pega o score do último dia para dar mais contexto
            score_hoje = df.iloc[-1]['score_compra']
            status_final = f"COMPRA ({contagem_compra} sinal/sinais nos últimos {dias_para_verificar} dias. Score hoje: {score_hoje:.0f})"
        elif contagem_venda > 0:
            score_hoje = df.iloc[-1]['score_venda']
            status_final = f"VENDA ({contagem_venda} sinal/sinais nos últimos {dias_para_verificar} dias. Score hoje: {score_hoje:.0f})"
            
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