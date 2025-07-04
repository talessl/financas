import pandas as pd
import pandas_ta as ta

class Indices:
    def __init__(self, dataframe_acao):
        if not isinstance(dataframe_acao, pd.DataFrame):
            raise TypeError("O dado fornecido deve ser um DataFrame do Pandas.")
        self.dados = dataframe_acao
    
    def didi(self):
        # Especificando para usar a coluna 'Close'
        self.dados.ta.sma(length=3, close='Close', append=True)
        self.dados.ta.sma(length=8, close='Close', append=True)
        self.dados.ta.sma(length=20, close='Close', append=True)

    def adx(self):
        # Especificando todas as colunas necessárias com nomes em MAIÚSCULAS
        self.dados.ta.adx(high='High', low='Low', close='Close', append=True)
    
    def rsi(self):
        self.dados.ta.rsi(close='Close', append=True)
    
    def stoch(self):
        self.dados.ta.stoch(high='High', low='Low', close='Close', append=True)

    def trix(self):
        self.dados.ta.trix(close='Close', append=True)
        
    def calcular_todos(self):
        # A classe agora está pronta para calcular tudo usando os nomes corretos
        self.didi()
        self.adx()
        self.rsi()
        self.stoch()
        self.trix()