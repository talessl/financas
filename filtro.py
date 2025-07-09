import yfinance as yf
import pandas_ta as ta
import acoes_b3

def verificar_rsi_sobrevenda(ticker: str, limite_rsi: int = 35)->bool:
    try:
        dados = yf.download(ticker, period="6mo", progress=False, auto_adjust=True)
        dados.columns = dados.columns.droplevel(1)

        dados.ta.rsi(append=True)
        ultimo_rsi = dados['RSI_14'].dropna().iloc[-1]
        return ultimo_rsi < limite_rsi
    except Exception as e:
            print(f"Ocorreu um erro ao processar {ticker}: {e}")
            return False


def verificar_stoch_sobrevenda(ticker: str, limite_stoch: int = 25)-> bool:
    try:

        dados = yf.download(ticker, period="6mo", progress=False, auto_adjust=True)
        dados.columns = dados.columns.droplevel(1)

        dados.ta.stoch(append=True)

        ultimo_stoch = dados['STOCHk_14_3_3'].dropna().iloc[-1]
        return ultimo_stoch < limite_stoch

    except Exception as e:
                print(f"Ocorreu um erro ao processar {ticker}: {e}")
                return False

def filtro_duplo(ticker: str) -> bool:
    if (verificar_rsi_sobrevenda(ticker) and verificar_rsi_sobrevenda(ticker)):
        return True

def filtragem(lista_acoes: str) -> str:
    resultado = []
    for acao in lista_acoes:
        if filtro_duplo(acao):
            resultado.append(acao)
    return resultado

acoes_hoje = acoes_b3.acoes_baratas()
acoes_stoch_rsi_filtradas = filtragem(acoes_hoje)
