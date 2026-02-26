from typing import List
from src.domain.value_objects.market_data import MarketData

class Acao: # Singular geralmente faz mais sentido para Entidade
    def __init__(self, ticker: str, historico: List[MarketData]):
        self.ticker = ticker
        self.historico = historico # Lista de objetos, não listas de floats soltos!

    # Agora sua Entidade tem PODER (Regras de Negócio)
    
    def obter_preco_medio(self) -> float:
        if not self.historico:
            return 0.0
        soma = sum(dado.close for dado in self.historico)
        return soma / len(self.historico)

    def obter_maxima_historica(self) -> float:
        return max(dado.high for dado in self.historico)
    
    def obter_minima_historica(self) -> float:
        if not self.historico: return 0.0
        return min(d.low for d in self.historico)