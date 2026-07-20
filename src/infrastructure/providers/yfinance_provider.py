import yfinance as yf
from datetime import date
from typing import List, Dict
from src.domain.provider_interface import IDataProvider
from src.domain.value_objects.market_data import MarketData
import pandas as pd
import pandas_ta as ta


class YFinanceProvider(IDataProvider):
    def _baixar_dados(self, ticker: str, inicio: date, fim: date) -> List[MarketData]:
        """Faz o download e envelopa os dados estritamente em objetos MarketData."""
        start_str = inicio.strftime('%Y-%m-%d')
        end_str = fim.strftime('%Y-%m-%d')

        df = yf.download(ticker, start=start_str, end=end_str, progress=False)

        if df.empty:
            return []

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)

        lista_market_data = []

        # Itera pelas linhas do DataFrame para criar os seus Value Objects reais
        for data_registro, linha in df.iterrows():
            # Lembrete: O yfinance traz as colunas com a primeira letra maiúscula ('Close', 'High', 'Low')
            # A data vem direto do índice (data_registro)
            dado = MarketData(
                data=data_registro.date() if hasattr(data_registro, 'date') else data_registro,
                close=float(linha['Close']),
                high=float(linha['High']),
                low=float(linha['Low'])
            )
            lista_market_data.append(dado)

        return lista_market_data

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

    def escanear_oportunidades(self, tickers: List[str], inicio: date, fim: date, preco_maximo: float) -> List[Dict]:
        """Método principal que orquestra todo o fluxo do scanner."""
        acoes_aprovadas = []

        for ticker in tickers:
            try:
                # 1. Download dos dados
                df = self._baixar_dados(ticker, inicio, fim)
                if df.empty:
                    continue

                # 2. Filtro de preço antecipado
                preco_atual = self._obter_preco_valido(df, preco_maximo)
                if preco_atual is None:
                    print(
                        f"  ✗ {ticker}: (Acima de R$ {preco_maximo:.2f}) - IGNORADO")
                    continue

                # 3. Cálculo matemático (só ocorre se passou no filtro de preço)
                df = self._calcular_indicadores(df)

                # 4. Logs de acompanhamento (opcional, mantido do seu código original)
                rsi_ultimo = df['RSI'].dropna().iloc[-1]
                stoch_d_ultimo = df['STOCHd_14_3_3'].dropna().iloc[-1]
                print(
                    f"  ➔ {ticker}: Preço R$ {preco_atual:.2f} | RSI: {rsi_ultimo:.2f} | Estocástico: {stoch_d_ultimo:.2f}")

                # 5. Validação da estratégia e montagem do resultado
                if self._verificar_estrategia(df):
                    dados_acao = self._montar_dicionario_aprovado(
                        ticker, df, preco_atual)
                    acoes_aprovadas.append(dados_acao)
                    print(f"  ✓✓ 🎯 {ticker} APROVADO NO SCANNER!")

            except Exception as e:
                print(f"Erro ao processar {ticker}: {e}")
                continue

        return acoes_aprovadas
