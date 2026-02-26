import yfinance as yf
from datetime import date
from typing import List
from src.domain.provider_interface import IDataProvider
from src.domain.value_objects.market_data import MarketData
import pandas as pd 
import pandas_ta as ta

class YFinanceProvider(IDataProvider):
    def buscar_dados(self, ticker: str, inicio: date, fim: date) -> List[MarketData]:

        start_str = inicio.strftime('%Y-%m-%d')
        end_str = fim.strftime('%Y-%m-%d')

        df = yf.download(ticker, start=start_str, end=end_str, progress=False)
        
        if df.empty:
            return []
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)

        resultado = []
        for index, row in df.iterrows():
            market_data = MarketData(
                data=index.date(),
                close=float(row['Close']),
                high=float(row['High']),
                low=float(row['Low'])
            )
            resultado.append(market_data)
            
        return resultado
    

    def filtrar_adx(self, tickers: list, inicio: date, fim: date, periodo: int = 14, limite: float = 20.0) -> List[str]:
        """
        Filtra tickers que possuem ADX acima do limite especificado.
        """
        tickers_aprovados = []
        
        
        for ticker in tickers:
            try:
                start_str = inicio.strftime('%Y-%m-%d')
                end_str = fim.strftime('%Y-%m-%d')

                df = yf.download(ticker, start=start_str, end=end_str, progress=False)
                
                
                if df.empty:
                    print(f"  └─ DataFrame vazio, pulando...")
                    continue
                
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.droplevel(1)
                
                
                # Calcular ADX usando pandas_ta
                adx_df = df.ta.adx(high='High', low='Low', close='Close', length=periodo)
                
                print(f"  └─ ADX calculado, shape: {adx_df.shape}")
                print(f"  └─ Colunas ADX: {adx_df.columns.tolist()}")
                
                # Pegar o último valor do ADX (mais recente)
                adx_ultimo = adx_df[f'ADX_{periodo}'].dropna().iloc[-1]
                
                print(f"  └─ ADX último valor: {adx_ultimo:.2f}")
                
                # Verificar se está acima do limite
                if adx_ultimo > limite:
                    tickers_aprovados.append(ticker)
                    print(f"  ✓ {ticker}: ADX = {adx_ultimo:.2f} - APROVADO")
                else:
                    print(f"  ✗ {ticker}: ADX = {adx_ultimo:.2f} (abaixo de {limite})")
                    
            except Exception as e:
                print(f"  ✗ ERRO ao processar {ticker}: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        return tickers_aprovados
    
    def filtrar_rsi(self, tickers: list, inicio: date, fim: date, periodo: int = 14, limite_min: float = 35.0, limite_max: float = 65.0) -> List[str]:
        """
        Filtra tickers que possuem RSI entre os limites especificados.
        
        Args:
            tickers: Lista de tickers para analisar
            inicio: Data inicial
            fim: Data final
            periodo: Período do RSI (padrão: 14)
            limite_min: Valor mínimo do RSI (padrão: 35.0)
            limite_max: Valor máximo do RSI (padrão: 65.0)
            
        Returns:
            Lista de tickers que passaram no filtro
        """
        tickers_aprovados = []
        
        
        for ticker in tickers:
            try:
                start_str = inicio.strftime('%Y-%m-%d')
                end_str = fim.strftime('%Y-%m-%d')

                df = yf.download(ticker, start=start_str, end=end_str, progress=False)
                
                
                if df.empty:
                    print(f"  └─ DataFrame vazio, pulando...")
                    continue
                
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.droplevel(1)
                
                # Calcular RSI usando pandas_ta
                df['RSI'] = df.ta.rsi(close='Close', length=periodo)
                
                # Pegar o último valor do RSI (mais recente)
                rsi_ultimo = df['RSI'].dropna().iloc[-1]
                
                print(f"  └─ RSI último valor: {rsi_ultimo:.2f}")
                
                # Verificar se está entre os limites
                if limite_min <= rsi_ultimo <= limite_max:
                    tickers_aprovados.append(ticker)
                    print(f"  ✓ {ticker}: RSI = {rsi_ultimo:.2f} - APROVADO")
                else:
                    print(f"  ✗ {ticker}: RSI = {rsi_ultimo:.2f} (fora do intervalo {limite_min}-{limite_max})")
                    
            except Exception as e:
                print(f"  ✗ ERRO ao processar {ticker}: {type(e).__name__}: {e}")
                continue
        
        print(f"[PROVIDER] Finalizou. {len(tickers_aprovados)} tickers aprovados")
        return tickers_aprovados