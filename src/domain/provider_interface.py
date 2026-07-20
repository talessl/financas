from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from src.domain.value_objects.market_data import MarketData
from datetime import date


class IDataProvider(ABC):

    @abstractmethod
    def _baixar_dados(self, ticker: str, inicio: date, fim: date) -> List[MarketData]:
        """
        Contrato: O mundo externo deve me dar datas concretas.
        Eu devolvo uma lista de dados de mercado estruturados.
        """
        pass

    @abstractmethod
    def _obter_preco_valido(self, dados: Any, preco_maximo: float) -> Optional[float]:
        """
        Valida se o preço atual está dentro do limite máximo estipulado.
        Retorna o preço se for válido, ou None caso contrário.
        """
        pass

    @abstractmethod
    def _calcular_indicadores(self, dados: Any) -> Any:
        """
        Calcula e acopla os indicadores técnicos (como RSI e Estocástico) 
        aos dados de mercado fornecidos.
        """
        pass

    @abstractmethod
    def _verificar_estrategia(self, dados: Any) -> bool:
        """
        Avalia as regras de negócio dos indicadores para decidir 
        se o ativo é uma oportunidade de compra/venda.
        """
        pass

    @abstractmethod
    def _montar_dicionario_aprovado(self, ticker: str, dados: Any, preco_atual: float) -> Dict[str, Any]:
        """
        Estrutura os dados finais do ativo aprovado no formato de dicionário
        esperado pela aplicação (incluindo dados históricos para gráficos).
        """
        pass

    @abstractmethod
    def escanear_oportunidades(self, tickers: List[str], inicio: date, fim: date, preco_maximo: float) -> List[Dict[str, Any]]:
        """
        Método orquestrador que utiliza as etapas anteriores para escanear
        uma lista de tickers e retornar as oportunidades que passaram nos filtros.
        """
        pass
