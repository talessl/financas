# Arquivo: main.py (PFR com Filtro de Tendência de Médias Móveis 9, 21, 72)
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import indices

# ===================================================================
# 1. PREPARAÇÃO DOS DADOS
# ===================================================================
print("Baixando e preparando os dados para AZEV3.SA...")
d1 = yf.download("AZEV3.SA", start="2024-01-01") # Ajustado o ano para ter mais dados

if d1.empty:
    print("Não foi possível baixar os dados. Verifique o ticker e a conexão.")
    exit()

if isinstance(d1.columns, pd.MultiIndex):
    d1.columns = d1.columns.droplevel(1)

print("Colunas dos dados:", d1.columns.to_list())

# <<< IMPORTANTE >>>
# Garanta que seu arquivo 'indices.py' está calculando as SMAs de 9, 21 e 72.
# O método 'calcular_todos()' deve gerar as colunas 'SMA_9', 'SMA_21' e 'SMA_72'.
acao = indices.Indices(dataframe_acao=d1)
acao.calcular_todos()
df = acao.dados

# ===================================================================
# 2. DEFINIÇÃO DAS CONDIÇÕES (PFR + FILTRO DE MÉDIAS)
# ===================================================================
print("Definindo condições e procurando por sinais de PFR filtrados pela tendência...")

# --- Condições do Padrão PFR (Gatilho) ---
# Condição PFR de Compra: Mínima menor que anterior, Fechamento maior que anterior.
cond_pfr_compra = (df['Low'] < df['Low'].shift(1)) & (df['Close'] > df['Close'].shift(1))
# Condição PFR de Venda: Máxima maior que anterior, Fechamento menor que anterior.
cond_pfr_venda = (df['High'] > df['High'].shift(1)) & (df['Close'] < df['Close'].shift(1))


# --- Condições das Médias (Filtro de Tendência) ---
# <<< NOVO: Filtro para só comprar se a tendência for de ALTA >>>
# A tendência é de alta se o preço está acima da média de 21 e a média de 21 está acima da de 72.
filtro_alta = (df['Close'] > df['SMA_21']) & (df['SMA_21'] > df['SMA_72'])

# <<< NOVO: Filtro para só vender se a tendência for de BAIXA >>>
# A tendência é de baixa se o preço está abaixo da média de 21 e a média de 21 está abaixo da de 72.
filtro_baixa = (df['Close'] < df['SMA_21']) & (df['SMA_21'] < df['SMA_72'])


# --- Combinação do Gatilho com o Filtro ---
# <<< ALTERADO: O sinal agora exige que a condição PFR E o filtro de tendência sejam verdadeiros >>>
sinal_compra = df[cond_pfr_compra & filtro_alta]
sinal_venda = df[cond_pfr_venda & filtro_baixa]


print(f"\nEncontrados {len(sinal_compra)} sinais de COMPRA (PFR com filtro de alta).")
if not sinal_compra.empty: print(sinal_compra.index.date)

print(f"\nEncontrados {len(sinal_venda)} sinais de VENDA (PFR com filtro de baixa).")
if not sinal_venda.empty: print(sinal_venda.index.date)

# ===================================================================
# 3. CRIAÇÃO DA VISUALIZAÇÃO COM OS SINAIS
# ===================================================================
print("\nCriando a visualização...")
dados_para_plotar = df.tail(252)

paineis_adicionais = [
    # <<< ALTERADO: Plotando as médias corretas (9, 21, 72) >>>
    mpf.make_addplot(dados_para_plotar[['SMA_9', 'SMA_21', 'SMA_72']], panel=0),

    # Painel do ADX para análise de contexto de tendência
    mpf.make_addplot(dados_para_plotar['ADX_14'], panel=2, color='black', width=1.2, ylabel='ADX'),
    mpf.make_addplot(dados_para_plotar['DMP_14'], panel=2, color='green', width=0.8, linestyle='--'),
    mpf.make_addplot(dados_para_plotar['DMN_14'], panel=2, color='red', width=0.8, linestyle='--'),
    mpf.make_addplot([25 for _ in range(len(dados_para_plotar))], panel=2, color='gray', linestyle='-.', width=0.7),
]

# Adiciona o marcador de COMPRA (código mantido, pois já funciona com a variável 'sinal_compra')
if not sinal_compra.empty:
    common_buy_dates = dados_para_plotar.index.intersection(sinal_compra.index)
    if not common_buy_dates.empty:
        marcadores_compra = np.full(len(dados_para_plotar), np.nan)
        marcadores_compra[dados_para_plotar.index.isin(common_buy_dates)] = dados_para_plotar.loc[common_buy_dates, 'Low'] * 0.98
        paineis_adicionais.append(mpf.make_addplot(marcadores_compra, type='scatter', marker='^', color='green', markersize=100, panel=0))

# Adiciona o marcador de VENDA (código mantido)
if not sinal_venda.empty:
    common_sell_dates = dados_para_plotar.index.intersection(sinal_venda.index)
    if not common_sell_dates.empty:
        marcadores_venda = np.full(len(dados_para_plotar), np.nan)
        marcadores_venda[dados_para_plotar.index.isin(common_sell_dates)] = dados_para_plotar.loc[common_sell_dates, 'High'] * 1.02
        paineis_adicionais.append(mpf.make_addplot(marcadores_venda, type='scatter', marker='v', color='red', markersize=100, panel=0))

# Plotando o gráfico final com o novo título
mpf.plot(dados_para_plotar,
         type='candle',
         style='yahoo',
         # <<< ALTERADO: Título mais descritivo da nova estratégia >>>
         title='AZEV3.SA - PFR com Filtro de Médias (9, 21, 72)',
         ylabel='Preço (R$)',
         volume=True,
         addplot=paineis_adicionais,
         figscale=1.8,
         panel_ratios=(8, 2, 3))

print("Visualização gerada com sucesso!")