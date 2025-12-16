import pandas as pd
import pandas_ta as ta

class Indices:
    def __init__(self, dataframe_acao):
        if not isinstance(dataframe_acao, pd.DataFrame):
            raise TypeError("O dado fornecido deve ser um DataFrame do Pandas.")
        if isinstance(dataframe_acao.columns, pd.MultiIndex):
            
            dataframe_acao.columns = dataframe_acao.columns.get_level_values(0)
        
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

    def pfr(self):
        self.dados.ta.sma(close='Close',length=9, append=True)
        self.dados.ta.sma(close='Close',length=21, append=True)
        self.dados.ta.sma(close='Close', length=72, append=True)
        
