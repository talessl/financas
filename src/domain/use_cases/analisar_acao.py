from src.domain.provider_interface import IDataProvider
from src.domain.entities.acoes import Acao
from datetime import date, timedelta
from typing import List, Dict


class AnalisarAcao:
    # AQUI acontece a Mágica da Injeção de Dependência.
    def __init__(self, provider: IDataProvider):
        self.provider = provider

    def buscar(self, ticker: str):
        hoje = date.today()
        inicio = hoje - timedelta(days=45)

        dados = self.provider.buscar_dados(ticker, inicio, hoje)
        if not dados:
            return None

        return Acao(ticker=ticker, historico=dados)

    def escanear_oportunidades(self, tickers: List[str], preco_maximo: float = 10.0) -> List[Dict]:
        """
        Coordena o scanner aplicando o filtro de preço máximo e indicadores técnicos.
        """
        fim = date.today()
        inicio = fim - timedelta(days=90)

        return self.provider.escanear_oportunidades(tickers, inicio, fim, preco_maximo)
