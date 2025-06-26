# Arquivo: main.py (Correção para o ValueError)
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import indices

# ===================================================================
# 1. PREPARAÇÃO DOS DADOS
# ===================================================================
print("Baixando e preparando os dados...")
dados = yf.download("PETR4.SA", start="2023-01-01")
dados.columns = dados.columns.droplevel(1)
print("Colunas simplificadas:", dados.columns.to_list())

petrobras = indices.Indices(dataframe_acao=dados)
petrobras.calcular_todos()
df = petrobras.dados

# ===================================================================
# 2. DEFINIÇÃO DAS CONDIÇÕES IDEAIS (LÓGICA DO SINAL)
# ===================================================================
print("Definindo condições e procurando por sinais ideais...")

# As colunas geradas pelo pandas-ta são maiúsculas quando se usa o strategy
cond_adx_compra = (df['ADX_14'] > 25) & (df['DMP_14'] > df['DMN_14'])
cond_didi_compra = (df['SMA_3'].shift(1) < df['SMA_8'].shift(1)) & (df['SMA_3'] > df['SMA_8']) & \
                   (df['SMA_3'].shift(1) < df['SMA_20'].shift(1)) & (df['SMA_3'] > df['SMA_20'])
cond_trix_compra = (df['TRIX_30_9'].shift(1) < 0) & (df['TRIX_30_9'] > 0)
cond_stoch_compra = (df['STOCHk_14_3_3'].shift(1) < df['STOCHd_14_3_3'].shift(1)) & \
                    (df['STOCHk_14_3_3'] > df['STOCHd_14_3_3']) & (df['STOCHk_14_3_3'] < 30)
cond_rsi_compra = df['RSI_14'] < 40
sinal_compra = df[cond_adx_compra & cond_didi_compra & cond_trix_compra & cond_stoch_compra & cond_rsi_compra]

cond_adx_venda = (df['ADX_14'] > 25) & (df['DMN_14'] > df['DMP_14'])
cond_didi_venda = (df['SMA_3'].shift(1) > df['SMA_8'].shift(1)) & (df['SMA_3'] < df['SMA_8']) & \
                  (df['SMA_3'].shift(1) > df['SMA_20'].shift(1)) & (df['SMA_3'] < df['SMA_20'])
cond_trix_venda = (df['TRIX_30_9'].shift(1) > 0) & (df['TRIX_30_9'] < 0)
cond_stoch_venda = (df['STOCHk_14_3_3'].shift(1) > df['STOCHd_14_3_3'].shift(1)) & \
                   (df['STOCHk_14_3_3'] < df['STOCHd_14_3_3']) & (df['STOCHk_14_3_3'] > 70)
cond_rsi_venda = df['RSI_14'] > 60
sinal_venda = df[cond_adx_venda & cond_didi_venda & cond_trix_venda & cond_stoch_venda & cond_rsi_venda]

print(f"\nEncontrados {len(sinal_compra)} sinais de COMPRA IDEAL.")
if not sinal_compra.empty: print(sinal_compra.index.date)
print(f"\nEncontrados {len(sinal_venda)} sinais de VENDA IDEAL.")
if not sinal_venda.empty: print(sinal_venda.index.date)

# ===================================================================
# 3. CRIAÇÃO DA VISUALIZAÇÃO COM OS SINAIS
# ===================================================================
print("\nCriando a visualização...")
dados_para_plotar = df.tail(252)

# --- A CORREÇÃO ESTÁ AQUI ---
# Começamos com os painéis que SEMPRE existirão
paineis_adicionais = [
    mpf.make_addplot(dados_para_plotar[['SMA_3', 'SMA_8', 'SMA_20']], panel=0),
    mpf.make_addplot(dados_para_plotar[['ADX_14', 'DMP_14', 'DMN_14']], panel=2, ylabel='ADX'),
    mpf.make_addplot([25 for i in range(len(dados_para_plotar))], panel=2, color='gray', linestyle='--'),
]

# SÓ adicionamos o marcador de COMPRA se houver sinais de compra
if not sinal_compra.empty:
    common_buy_dates = dados_para_plotar.index.intersection(sinal_compra.index)
    if not common_buy_dates.empty:
        marcadores_compra = np.full(len(dados_para_plotar), np.nan)
        marcadores_compra[dados_para_plotar.index.isin(common_buy_dates)] = dados_para_plotar.loc[common_buy_dates, 'Low'] * 0.98
        paineis_adicionais.append(mpf.make_addplot(marcadores_compra, type='scatter', marker='^', color='green', markersize=100, panel=0))

# SÓ adicionamos o marcador de VENDA se houver sinais de venda
if not sinal_venda.empty:
    common_sell_dates = dados_para_plotar.index.intersection(sinal_venda.index)
    if not common_sell_dates.empty:
        marcadores_venda = np.full(len(dados_para_plotar), np.nan)
        marcadores_venda[dados_para_plotar.index.isin(common_sell_dates)] = dados_para_plotar.loc[common_sell_dates, 'High'] * 1.02
        paineis_adicionais.append(mpf.make_addplot(marcadores_venda, type='scatter', marker='v', color='red', markersize=100, panel=0))

# Plotando o gráfico final
mpf.plot(dados_para_plotar, 
         type='candle', 
         style='yahoo',
         title='PETR4.SA - Sinais de Entrada/Saída Ideais',
         ylabel='Preço (R$)',
         volume=True, 
         addplot=paineis_adicionais,
         figscale=1.8,
         panel_ratios=(8, 2, 3))

print("Visualização gerada com sucesso!")