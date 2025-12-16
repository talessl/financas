import indices
import acoesB3
import yfinance as yf
import pandas as pd


acoes = acoesB3.acoes_baratas()


def filtro_agressivo_otimizado(tickers):
    """
    FILTRO AGRESSIVO OTIMIZADO: Baixa dados uma vez só
    """
    print(">> Aplicando Filtro Agressivo Otimizado...\n")
    print(f">> Baixando dados de {len(tickers)} acoes (pode demorar 1-2 min)...\n")
    
    # Baixar TODOS os dados de uma vez
    dados_todos = yf.download(
        tickers=tickers,
        period="6mo",
        progress=True,  # Mostrar progresso
        group_by='ticker'
    )
    
    resultados = {
        'didi': [],
        'adx': [],
        'rsi': [],
        'stoch': [],
        'trix': []
    }
    
    print("\n>> Analisando indicadores...\n")
    
    for ticker in tickers:
        try:
            # Pegar dados do ticker específico
            if len(tickers) == 1:
                dados = dados_todos
            else:
                dados = dados_todos[ticker]
            
            # Criar objeto de índices uma vez
            metodo = indices.Indices(dados)
            
            # Calcular todos os indicadores
            metodo.didi()
            metodo.pfr()
            metodo.adx()
            metodo.rsi()
            metodo.stoch()
            metodo.trix()
            
            # Pegar valores
            preco = metodo.dados['Close'].iloc[-1]
            
            # 1. DIDI
            sma3 = metodo.dados['SMA_3'].iloc[-1]
            sma8 = metodo.dados['SMA_8'].iloc[-1]
            sma20 = metodo.dados['SMA_20'].iloc[-1]
            sma72 = metodo.dados['SMA_72'].iloc[-1]
            
            if sma3 > sma8 > sma20 and preco > sma72:
                resultados['didi'].append(ticker)
            
            # 2. ADX
            adx = metodo.dados['ADX_14'].iloc[-1]
            dmp = metodo.dados['DMP_14'].iloc[-1]
            dmn = metodo.dados['DMN_14'].iloc[-1]
            
            if adx > 25 and dmp > dmn:
                resultados['adx'].append(ticker)
            
            # 3. RSI
            rsi = metodo.dados['RSI_14'].iloc[-1]
            
            if 40 < rsi < 70:
                resultados['rsi'].append(ticker)
            
            # 4. STOCH
            k_atual = metodo.dados['STOCHk_14_3_3'].iloc[-1]
            d_atual = metodo.dados['STOCHd_14_3_3'].iloc[-1]
            k_anterior = metodo.dados['STOCHk_14_3_3'].iloc[-2]
            d_anterior = metodo.dados['STOCHd_14_3_3'].iloc[-2]
            
            cruzamento = (k_anterior <= d_anterior) and (k_atual > d_atual)
            if cruzamento and k_atual < 80:
                resultados['stoch'].append(ticker)
            
            # 5. TRIX
            trix_atual = metodo.dados['TRIX_30_9'].iloc[-1]
            trix_anterior = metodo.dados['TRIX_30_9'].iloc[-2]
            
            if trix_atual > 0 or (trix_anterior < 0 and trix_atual > trix_anterior):
                resultados['trix'].append(ticker)
        
        except Exception as e:
            pass  # Ignorar erros silenciosamente
    
    # Contar sinais por ação
    contagem = {}
    for lista in resultados.values():
        for ticker in lista:
            contagem[ticker] = contagem.get(ticker, 0) + 1
    
    # Filtrar com 4+ sinais
    acoes_aprovadas = [t for t, c in contagem.items() if c >= 4]
    
    print(f">> Resultados:")
    print(f"   Didi Agulhada: {len(resultados['didi'])} acoes")
    print(f"   ADX Forte: {len(resultados['adx'])} acoes")
    print(f"   RSI Medio: {len(resultados['rsi'])} acoes")
    print(f"   Stoch Compra: {len(resultados['stoch'])} acoes")
    print(f"   TRIX Positivo: {len(resultados['trix'])} acoes")
    print(f"\n>> Acoes aprovadas (4+ sinais): {len(acoes_aprovadas)}\n")
    print(f"Lista de aprovadas: {acoes_aprovadas}")
    
    return acoes_aprovadas

tickers = acoes
# Usar a versão otimizada
resultados_finais = filtro_agressivo_otimizado(tickers)