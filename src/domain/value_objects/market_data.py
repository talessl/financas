from dataclasses import dataclass
from datetime import date

# dados puros sem lógica complexa

@dataclass
class MarketData:
    """Representa o preço em um momento específico (Value Object)"""
    data: date
    close: float
    high: float
    low: float
