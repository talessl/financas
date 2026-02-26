from abc import ABC, abstractmethod
from typing import List
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
    
    
    
    def filtrar_adx(self, tickers: list, inicio: date, fim: date, periodo: int = 14, limite: float = 20.0) -> List[MarketData]:
        """
        Filtrar acoes com adx definido pelo usuario
        """
        pass
    
    def filtrar_rsi(self, tickers: list, inicio: date, fim: date, periodo: int = 14, limite_min: float = 35.0, limite_max: float = 65.0) -> List[str]:
        """
        Filtrar acoes com rsi definido pelo usuar
        """
        pass