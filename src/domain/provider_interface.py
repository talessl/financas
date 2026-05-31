from abc import ABC, abstractmethod
from typing import List, Dict
from src.domain.value_objects.market_data import MarketData
from datetime import date


class IDataProvider(ABC):
    @abstractmethod
    def buscar_dados(self, ticker: str, inicio: date, fim: date) -> List[MarketData]:
        """
        Contrato: O mundo externo deve me dar datas concretas.
        Eu devolvo uma lista de objetos MarketData tipados.
        """
        pass

    @abstractmethod
    def escanear_oportunidades(self, tickers: List[str], inicio: date, fim: date, preco_maximo: float) -> List[Dict]:
        pass
