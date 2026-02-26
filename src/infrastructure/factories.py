import os
from src.infrastructure.providers.yfinance_provider import YFinanceProvider

def criar_provider():
    tipo = os.getenv("PROVIDER_TYPE", "YAHOO")

    if tipo == "YAHOO":
        return YFinanceProvider()
    else:
        raise Exception("Provider desconhecido")