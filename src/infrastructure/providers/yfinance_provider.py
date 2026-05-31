import yfinance as yf
from datetime import date
from typing import List, Dict
from src.domain.provider_interface import IDataProvider
from src.domain.value_objects.market_data import MarketData
import pandas as pd
import pandas_ta as ta


class YFinanceProvider(IDataProvider):
    def buscar_dados(self, ticker: str, inicio: date, fim: date) -> List[MarketData]:

        start_str = inicio.strftime('%Y-%m-%d')
        end_str = fim.strftime('%Y-%m-%d')

        df = yf.download(ticker, start=start_str, end=end_str, progress=False)

        if df.empty:
            return []

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)

        resultado = []
        for index, row in df.iterrows():
            market_data = MarketData(
                data=index.date(),
                close=float(row['Close']),
                high=float(row['High']),
                low=float(row['Low'])
            )
            resultado.append(market_data)

        return resultado

    def escanear_oportunidades(self, tickers: List[str], inicio: date, fim: date, preco_maximo: float) -> List[Dict]:
        acoes_aprovadas = []

        for ticker in tickers:
            try:
                start_str = inicio.strftime('%Y-%m-%d')
                end_str = fim.strftime('%Y-%m-%d')

                df = yf.download(ticker, start=start_str,
                                 end=end_str, progress=False)
                if df.empty:
                    continue

                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.droplevel(1)

                # --- OTIMIZAÇÃO: Filtro de preço antecipado ---
                preco_atual = float(df['Close'].dropna().iloc[-1])

                if preco_atual > preco_maximo:
                    print(
                        f"  ✗ {ticker}: R$ {preco_atual:.2f} (Acima de R$ {preco_maximo:.2f}) - IGNORADO")
                    continue  # Pula direto para a próxima ação do laço

                # Se o preço for menor ou igual a 10, aí sim calculamos o RSI e Estocástico
                df['RSI'] = df.ta.rsi(close='Close', length=14)
                stoch = df.ta.stoch(high='High', low='Low',
                                    close='Close', k=14, d=3, smooth_k=3)
                df = pd.concat([df, stoch], axis=1)

                rsi_ultimo = df['RSI'].dropna().iloc[-1]
                stoch_d_ultimo = df['STOCHd_14_3_3'].dropna().iloc[-1]

                print(
                    f"  ➔ {ticker}: Preço R$ {preco_atual:.2f} | RSI: {rsi_ultimo:.2f} | Estocástico: {stoch_d_ultimo:.2f}")

                if rsi_ultimo < 30 and stoch_d_ultimo < 20:
                    acoes_aprovadas.append({
                        "ticker": ticker,
                        "nome": ticker.replace('.SA', ''),
                        "setor": "Filtro < R$10",
                        "preco": preco_atual
                    })
                    print(f"  ✓✓ 🎯 {ticker} APROVADO NO SCANNER!")

            except Exception as e:
                print(f"Erro ao processar {ticker}: {e}")
                continue

        return acoes_aprovadas
