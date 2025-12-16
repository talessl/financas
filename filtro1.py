import indices
import acoesB3
import yfinance as yf
import pandas as pd


acoes = acoesB3.acoes_baratas()

dados = yf.download(
        tickers=acoes,
        period="3mo",
        progress=False
    )

def analisar_ifr_abaixo(tickers, limite=30):
    """
    Filtra ações com IFR(RSI) abaixo do limite
    """
    resultados = []

    for ticker in tickers:
        try:
            # Baixar dados
            dados = yf.download(
                tickers=ticker,
                period="3mo",  # ← 3 meses
                progress=False
            )
            
            # Calcular Stochastic
            metodo = indices.Indices(dados)
            metodo.rsi()
            
            # Pegar último valor
            ultimo_rsi = metodo.dados['RSI_14'].iloc[-1]
            ultimo_close = metodo.dados['Close'].iloc[-1]
            # Verificar se está abaixo do limite
            if ultimo_rsi < limite:
                resultados.append({
                    'Ticker': ticker,
                    'Preço': ultimo_close,
                    'RSI': round(ultimo_rsi, 2),
                    'Status': 'ABAIXO'
                })
        
        except Exception as e:
            print(f"Erro em {ticker}: {e}")

    return pd.DataFrame(resultados)


def analisar_stoch_sobrevenda(tickers, limite=20):
    """
    Filtra ações com Stochastic abaixo do limite (sobrevenda)
    """
    resultados = []
    
    for ticker in tickers:
        try:
            # Baixar dados
            dados = yf.download(
                tickers=ticker,
                period="3mo",  # ← 3 meses
                progress=False
            )
            
            # Calcular Stochastic
            metodo = indices.Indices(dados)
            metodo.stoch()
            
            # Pegar último valor
            ultimo_k = metodo.dados['STOCHk_14_3_3'].iloc[-1]
            ultimo_d = metodo.dados['STOCHd_14_3_3'].iloc[-1]
            ultimo_close = metodo.dados['Close'].iloc[-1]
            
            # Verificar se está em sobrevenda
            if ultimo_k < limite and ultimo_d < limite:
                resultados.append({
                    'Ticker': ticker,
                    'Preço': ultimo_close,
                    'Stoch K': round(ultimo_k, 2),
                    'Stoch D': round(ultimo_d, 2),
                    'Status': 'SOBREVENDA'
                })
        
        except Exception as e:
            print(f"Erro em {ticker}: {e}")
    
    return pd.DataFrame(resultados)

def intersecacao_listas(lista1, lista2):
    """
    Retorna a interseção entre duas listas
    """
    return list(set(lista1) & set(lista2))


# Exemplo de uso
tickers = acoes
resultado1 = analisar_stoch_sobrevenda(tickers)
resultado2 = analisar_ifr_abaixo(tickers)
resultados_finais = intersecacao_listas(resultado1['Ticker'], resultado2['Ticker'])
print("Ações em sobrevenda (Stochastic < 20) e IFR < 30:")
print(resultados_finais)

