# Arquivo: indices.py (VERSÃO ATUALIZADA)
import pandas as pd
import pandas_ta as ta

class Indices:
    def __init__(self, dataframe_acao):
        if not isinstance(dataframe_acao, pd.DataFrame):
            raise TypeError("O dado fornecido deve ser um DataFrame do Pandas.")
        self.dados = dataframe_acao
    
    # Adicionamos os métodos para Didi e ADX
    def didi(self):
        self.dados.ta.sma(length=3, append=True)
        self.dados.ta.sma(length=8, append=True)
        self.dados.ta.sma(length=20, append=True)

    def adx(self):
        self.dados.ta.adx(append=True)
    
    def rsi(self):
        self.dados.ta.rsi(append=True)
    
    def stoch(self):
        self.dados.ta.stoch(append=True)

    def trix(self):
        self.dados.ta.trix(append=True)
        
    def calcular_todos(self):
        print("\nCalculando todos os indicadores...")
        self.didi() # <-- Adicionado
        self.adx()  # <-- Adicionado
        self.rsi()
        self.stoch()
        self.trix()
        print("Cálculos finalizados.")