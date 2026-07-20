from src.domain.value_objects.market_data import MarketData
import pandas as pd
import pandas_ta as ta
from typing import List, Tuple


class Acao:
    def __init__(self, ticker: str, historico: List[MarketData]):
        self.ticker = ticker
        self.historico = historico

    def obter_preco_medio(self) -> float:
        if not self.historico:
            return 0.0
        soma = sum(dado.close for dado in self.historico)
        return soma / len(self.historico)

    def obter_maxima_historica(self) -> float:
        return max(dado.high for dado in self.historico)

    def obter_minima_historica(self) -> float:
        if not self.historico:
            return 0.0
        return min(d.low for d in self.historico)

    def _converter_para_dataframe(self) -> pd.DataFrame:
        """Método privado (Helper) para facilitar cálculos matemáticos no domínio."""
        if not self.historico:
            return pd.DataFrame()

        return pd.DataFrame({
            'close': [d.close for d in self.historico],
            'high': [d.high for d in self.historico],
            'low': [d.low for d in self.historico]
        })

    def calcular_rsi(self, periodos: int = 14) -> List[float]:
        """Calcula o Índice de Força Relativa (RSI)."""
        df = self._converter_para_dataframe()
        if df.empty or len(df) < periodos:
            return [0] * len(self.historico)

        df.ta.rsi(length=periodos, append=True)
        return df[f'RSI_{periodos}'].fillna(0).tolist()

    def calcular_estocastico(self) -> Tuple[List[float], List[float]]:
        """Calcula o Estocástico Lento (14, 3, 3) e retorna as linhas K e D."""
        df = self._converter_para_dataframe()
        if df.empty or len(df) < 14:
            zerados = [0] * len(self.historico)
            return zerados, zerados

        df.ta.stoch(append=True)
        df = df.fillna(0)
        return df['STOCHk_14_3_3'].tolist(), df['STOCHd_14_3_3'].tolist()

    def calcular_didi_index(self) -> Tuple[List[float], List[float]]:
        """Calcula as Agulhadas do Didi (Médias 3, 8 e 20). Retorna (Curta, Longa)."""
        df = self._converter_para_dataframe()
        if df.empty or len(df) < 20:
            zerados = [0] * len(self.historico)
            return zerados, zerados

        sma_3 = df.ta.sma(length=3)
        sma_8 = df.ta.sma(length=8)
        sma_20 = df.ta.sma(length=20)

        # A Média de 8 é o eixo zero. A curta e a longa orbitam ao redor dela.
        curta = (sma_3 - sma_8).fillna(0).tolist()
        longa = (sma_20 - sma_8).fillna(0).tolist()

        return curta, longa
