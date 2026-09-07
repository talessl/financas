import yfinance as yf
from datetime import date
from typing import List, Dict
from src.domain.provider_interface import IDataProvider
import pandas as pd


class YFinanceProvider(IDataProvider):
    def _baixar_dados(self, ticker: str, inicio: date, fim: date):
        """Faz o download e retorna o DataFrame do Pandas puro para análise técnica."""
        start_str = inicio.strftime('%Y-%m-%d')
        end_str = fim.strftime('%Y-%m-%d')

        df = yf.download(ticker, start=start_str, end=end_str, progress=False)

        if df.empty:
            return df

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)

        return df

    def _obter_preco_valido(self, df: pd.DataFrame, preco_maximo: float) -> float:
        """Retorna o preço atual se estiver dentro do limite, ou None caso contrário."""
        preco_atual = float(df['Close'].dropna().iloc[-1])
        if preco_atual > preco_maximo:
            return None
        return preco_atual

    def _calcular_indicadores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona as colunas de RSI e Estocástico ao DataFrame."""
        df['RSI'] = df.ta.rsi(close='Close', length=14)
        stoch = df.ta.stoch(high='High', low='Low',
                            close='Close', k=14, d=3, smooth_k=3)

        return pd.concat([df, stoch], axis=1)

    def _verificar_estrategia(self, df: pd.DataFrame) -> bool:
        """Checa se os indicadores atendem aos critérios de compra."""
        rsi_ultimo = df['RSI'].dropna().iloc[-1]
        stoch_d_ultimo = df['STOCHd_14_3_3'].dropna().iloc[-1]

        return rsi_ultimo < 30 and stoch_d_ultimo < 20

    def _montar_dicionario_aprovado(self, ticker: str, df: pd.DataFrame, preco_atual: float) -> Dict:
        """Gera o dicionário final com os dados de gráficos e máximas/mínimas."""
        df_30_dias = df.tail(30)

        return {
            "ticker": ticker,
            "nome": ticker.replace('.SA', ''),
            "setor": "Filtro < Preço Max",
            "preco_atual": preco_atual,
            "maxima": float(df_30_dias['High'].max()),
            "minima": float(df_30_dias['Low'].min()),
            "datas_grafico": [data.strftime("%d/%m") for data in df_30_dias.index],
            "precos_grafico": [float(preco) for preco in df_30_dias['Close']]
        }

    def escanear_oportunidades(self, tickers: List[str], inicio: date, fim: date, preco_maximo: float):
        """Método principal que orquestra todo o fluxo do scanner."""
        for ticker in tickers:
            try:
                df = self._baixar_dados(ticker, inicio, fim)
                if df.empty:
                    continue

                preco_atual = self._obter_preco_valido(df, preco_maximo)
                if preco_atual is None:
                    yield f"✗ {ticker}: (Acima de R$ {preco_maximo:.2f}) - IGNORADO"
                    continue

                df = self._calcular_indicadores(df)

                rsi_ultimo = df['RSI'].dropna().iloc[-1]
                stoch_d_ultimo = df['STOCHd_14_3_3'].dropna().iloc[-1]

                # Entrega o texto do log para a tela
                yield f"➔ {ticker}: Preço R$ {preco_atual:.2f} | RSI: {rsi_ultimo:.2f} | Estoc: {stoch_d_ultimo:.2f}"

                if self._verificar_estrategia(df):
                    dados_acao = self._montar_dicionario_aprovado(
                        ticker, df, preco_atual)
                    yield f"✓✓ 🎯 {ticker} APROVADO NO SCANNER!"
                    # Entrega um dicionário quando achar uma ação válida
                    yield {"acao_aprovada": dados_acao}

            except Exception as e:
                yield f"Erro ao processar {ticker}: {e}"
                continue
