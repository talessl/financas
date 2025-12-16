import indices
import acoesB3
import yfinance as yf
import pandas as pd

acoes = acoesB3.acoes_baratas()

def filtro_agressivo_otimizado(tickers, volume_minimo=100000, dias_analise=20):
    """
    FILTRO AGRESSIVO OTIMIZADO com filtro de liquidez
    
    Args:
        tickers: lista de tickers
        volume_minimo: volume médio mínimo diário (padrão: 100k)
        dias_analise: dias para calcular médias (padrão: 20)
    """
    print(">> Aplicando Filtro Agressivo Otimizado...\n")
    print(f">> Baixando dados de {len(tickers)} ações (pode demorar 1-2 min)...\n")
    
    # Baixar TODOS os dados de uma vez
    dados_todos = yf.download(
        tickers=tickers,
        period="6mo",
        progress=True,
        group_by='ticker'
    )
    
    resultados = {
        'didi': [],
        'adx': [],
        'rsi': [],
        'stoch': [],
        'trix': []
    }
    
    # NOVO: Rastreamento de liquidez
    acoes_liquidas = []
    acoes_sem_liquidez = []
    
    print("\n>> Analisando liquidez e indicadores...\n")
    
    for ticker in tickers:
        try:
            # Pegar dados do ticker específico
            if len(tickers) == 1:
                dados = dados_todos
            else:
                dados = dados_todos[ticker]
            
            # ============================================
            # FILTRO DE LIQUIDEZ (NOVO)
            # ============================================
            
            # 1. Volume médio dos últimos N dias
            volume_medio = dados['Volume'].tail(dias_analise).mean()
            
            # 2. Verificar dias sem negociação (volume = 0)
            dias_sem_volume = (dados['Volume'].tail(dias_analise) == 0).sum()
            percentual_dias_mortos = (dias_sem_volume / dias_analise) * 100
            
            # 3. Volatilidade mínima (preço se move?)
            volatilidade = dados['Close'].tail(dias_analise).std() / dados['Close'].tail(dias_analise).mean()
            
            # 4. Spread médio (diferença High-Low / Close)
            spread_medio = ((dados['High'] - dados['Low']) / dados['Close']).tail(dias_analise).mean()
            
            # CRITÉRIOS DE LIQUIDEZ
            tem_liquidez = (
                volume_medio >= volume_minimo and  # Volume suficiente
                percentual_dias_mortos < 20 and     # Máximo 20% dias parados
                volatilidade > 0.01 and             # Mínimo 1% de volatilidade
                spread_medio > 0.005                # Mínimo 0.5% de spread
            )
            
            if not tem_liquidez:
                acoes_sem_liquidez.append({
                    'ticker': ticker,
                    'volume_medio': int(volume_medio),
                    'dias_parados': dias_sem_volume,
                    'volatilidade': f"{volatilidade:.2%}"
                })
                continue  # Pular esta ação
            
            acoes_liquidas.append(ticker)
            
            # ============================================
            # ANÁLISE TÉCNICA (código original)
            # ============================================
            
            metodo = indices.Indices(dados)
            
            metodo.didi()
            metodo.pfr()
            metodo.adx()
            metodo.rsi()
            metodo.stoch()
            metodo.trix()
            
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
            pass
    
    # Contar sinais por ação (somente nas líquidas)
    contagem = {}
    for lista in resultados.values():
        for ticker in lista:
            contagem[ticker] = contagem.get(ticker, 0) + 1
    
    acoes_aprovadas = [t for t, c in contagem.items() if c >= 4]
    
    # ============================================
    # RELATÓRIO DETALHADO
    # ============================================
    
    print(f"\n{'='*60}")
    print(f"FILTRO DE LIQUIDEZ:")
    print(f"{'='*60}")
    print(f"Ações líquidas: {len(acoes_liquidas)}")
    print(f"Ações sem liquidez: {len(acoes_sem_liquidez)}")
    print(f"   (Volume < {volume_minimo:,} ou >20% dias parados)")
    
    if acoes_sem_liquidez:
        print(f"\n>> Top 10 ações EXCLUÍDAS por baixa liquidez:")
        df_sem_liquidez = pd.DataFrame(acoes_sem_liquidez).head(10)
        print(df_sem_liquidez.to_string(index=False))
    
    print(f"\n{'='*60}")
    print(f"ANÁLISE TÉCNICA (somente ações líquidas):")
    print(f"{'='*60}")
    print(f"   Didi Agulhada: {len(resultados['didi'])} ações")
    print(f"   ADX Forte: {len(resultados['adx'])} ações")
    print(f"   RSI Médio: {len(resultados['rsi'])} ações")
    print(f"   Stoch Compra: {len(resultados['stoch'])} ações")
    print(f"   TRIX Positivo: {len(resultados['trix'])} ações")
    
    print(f"\n{'='*60}")
    print(f"RESULTADO FINAL:")
    print(f"{'='*60}")
    print(f">> Ações aprovadas (4+ sinais + liquidez): {len(acoes_aprovadas)}\n")
    print(f"Lista final: {acoes_aprovadas}")
    
    return acoes_aprovadas


# USO:
tickers = acoes

# Opção 1: Volume mínimo conservador (100k por dia)
resultados_finais = filtro_agressivo_otimizado(tickers, volume_minimo=100000)

# Opção 2: Volume mais rigoroso (500k por dia) para ações muito líquidas
# resultados_finais = filtro_agressivo_otimizado(tickers, volume_minimo=500000)

# Opção 3: Volume mais flexível (50k) para small caps
# resultados_finais = filtro_agressivo_otimizado(tickers, volume_minimo=50000)