import yfinance as yf
import pandas_ta as ta
import pandas as pd




PRECO_MAXIMO = 10.0


# ===================================================================
# 2. EXECUÇÃO DO SCANNER
# ===================================================================

def acoes_baratas():
    print(f"Buscando ações na lista com preço abaixo de R$ {PRECO_MAXIMO:.2f}...")

    acoes = [
    "AALR3.SA", "ABCB4.SA", "ABEV3.SA", "AERI3.SA", "AFLT3.SA", "AGRO3.SA", "AGXY3.SA",
    "ALLD3.SA", "ALPA3.SA", "ALPA4.SA", "ALPK3.SA", "ALOS3.SA", "ALUP11.SA", "ALUP3.SA",
    "ALUP4.SA", "AMAR3.SA", "AMBP3.SA", "AMER3.SA", "AMOB3.SA", "ANIM3.SA", "ARML3.SA",
    "ARZZ3.SA", "ASAI3.SA", "ATED3.SA", "AURE3.SA", "AVLL3.SA", "AZEV3.SA", "AZEV4.SA",
    "AZUL4.SA", "B3SA3.SA", "BALM3.SA", "BALM4.SA", "BAUH4.SA", "BAZA3.SA", "BBAS3.SA",
    "BBDC3.SA", "BBDC4.SA", "BBSE3.SA", "BDLL4.SA", "BEES3.SA", "BEES4.SA", "BEEF3.SA",
    "BGIP3.SA", "BGIP4.SA", "BHIA3.SA", "BIED3.SA", "BIOM3.SA", "BLAU3.SA", "BMEB3.SA",
    "BMEB4.SA", "BMGB4.SA", "BMKS3.SA", "BMOB3.SA", "BNBR3.SA", "BOBR4.SA", "BPAC11.SA",
    "BPAC3.SA", "BPAC5.SA", "BPAN4.SA", "BRAP3.SA", "BRAP4.SA", "BRBI11.SA", "BRFS3.SA",
    "BRKM3.SA", "BRKM5.SA", "BRKM6.SA", "BRSR3.SA", "BRSR5.SA", "BRSR6.SA", "BSLI3.SA",
    "BSLI4.SA", "CAMB3.SA", "CAML3.SA", "CASH3.SA", "CBAV3.SA", "CBEE3.SA", "CCTY3.SA",
    "CEDO3.SA", "CEDO4.SA", "CEED3.SA", "CEEB3.SA", "CEBR6.SA", "CGAS3.SA", "CGAS5.SA",
    "CGRA3.SA", "CGRA4.SA", "CIEL3.SA", "CLSC3.SA", "CLSC4.SA", "CMIG3.SA", "CMIG4.SA",
    "CMIN3.SA", "COCE3.SA", "COCE5.SA", "COGN3.SA", "CPFE3.SA", "CPLE3.SA", "CPLE5.SA",
    "CPLE6.SA", "CRPG3.SA", "CRPG5.SA", "CRPG6.SA", "CSAN3.SA", "CSED3.SA", "CSMG3.SA",
    "CSNA3.SA", "CSUD3.SA", "CTKA3.SA", "CTKA4.SA", "CTSA3.SA", "CTSA4.SA", "CURY3.SA",
    "CVCB3.SA", "CXSE3.SA", "CYRE3.SA", "DASA3.SA", "DESK3.SA", "DEXP3.SA", "DEXP4.SA",
    "DIRR3.SA", "DOHL4.SA", "DOTZ3.SA", "DTCY3.SA", "DXCO3.SA", "ECOR3.SA", "EGIE3.SA",
    "EKTR3.SA", "EKTR4.SA", "ELET3.SA", "ELET6.SA", "EMAE3.SA", "EMAE4.SA", "EMBR3.SA",
    "ENEV3.SA", "ENGI11.SA", "ENGI4.SA", "ENJU3.SA", "ENMT3.SA", "ENMT4.SA", "EPAR3.SA",
    "EQTL3.SA", "ESPA3.SA", "ESTR4.SA", "ETER3.SA", "EUCA3.SA", "EUCA4.SA", "EVEN3.SA",
    "EZTC3.SA", "FESA3.SA", "FESA4.SA", "FHER3.SA", "FIEI3.SA", "FIQE3.SA", "FLRY3.SA",
    "FRAS3.SA", "FRIO3.SA", "GEPA3.SA", "GEPA4.SA", "GFSA3.SA", "GGBR3.SA", "GGBR4.SA",
    "GGPS3.SA", "GMAT3.SA", "GOAU3.SA", "GOAU4.SA", "GRND3.SA", "GSHP3.SA", "GUAR3.SA",
    "HAGA3.SA", "HAGA4.SA", "HAPV3.SA", "HBRE3.SA", "HBSA3.SA", "HBTS5.SA", "HETA4.SA",
    "HOOT4.SA", "HYPE3.SA", "IGTI11.SA", "INEP3.SA", "INEP4.SA", "INTB3.SA", "IRBR3.SA",
    "ITSA3.SA", "ITSA4.SA", "ITUB3.SA", "ITUB4.SA", "JALL3.SA", "JFEN3.SA", "JHSF3.SA",
    "JOPA3.SA", "KEPL3.SA", "KLBN11.SA", "KLBN3.SA", "KLBN4.SA", "LAND3.SA", "LAVV3.SA",
    "LEVE3.SA", "LIGT3.SA", "LJQQ3.SA", "LOGG3.SA", "LOGN3.SA", "LPSB3.SA", "LREN3.SA",

    "LUPA3.SA", "LUXM4.SA", "LVTC3.SA", "LWSA3.SA", "MAPT4.SA", "MATD3.SA", "MDIA3.SA",
    "MDNE3.SA", "MEAL3.SA", "MELK3.SA", "MGLU3.SA", "MGEL4.SA", "MILS3.SA", "MLAS3.SA",
    "MNDL3.SA", "MNPR3.SA", "MOAR3.SA", "MRFG3.SA", "MRVE3.SA", "MTSA4.SA", "MULT3.SA",
    "MWET4.SA", "MYPK3.SA", "NEOE3.SA", "NEXP3.SA", "NGRD3.SA", "NORD3.SA", "NTCO3.SA",
    "NUTR3.SA", "ODPV3.SA", "OFSA3.SA", "OIBR3.SA", "OIBR4.SA", "ONCO3.SA", "OPCT3.SA",
    "ORVR3.SA", "OSXB3.SA", "PATI3.SA", "PATI4.SA", "PCAR3.SA", "PDGR3.SA", "PDTC3.SA",
    "PEAB4.SA", "PETR3.SA", "PETR4.SA", "PETZ3.SA", "PFRM3.SA", "PGMN3.SA", "PINE3.SA",
    "PINE4.SA", "PLPL3.SA", "PLAS3.SA", "PNVL3.SA", "POMO3.SA", "POMO4.SA", "PORT3.SA",
    "POSI3.SA", "PSSA3.SA", "PTBL3.SA", "PTNT3.SA", "PTNT4.SA", "QUAL3.SA", "RADL3.SA",
    "RAIL3.SA", "RAIZ4.SA", "RANI3.SA", "RAPT3.SA", "RAPT4.SA", "RCSL3.SA", "RCSL4.SA",
    "RDNI3.SA", "RDOR3.SA", "RECV3.SA", "REDE3.SA", "RENT3.SA", "RNEW11.SA", "RNEW3.SA",
    "RNEW4.SA", "ROMI3.SA", "RPAD3.SA", "RPMG3.SA", "RSID3.SA", "RSUL4.SA", "SANB11.SA",
    "SANB3.SA", "SANB4.SA", "SAPR11.SA", "SAPR3.SA", "SAPR4.SA", "SBFG3.SA", "SBSP3.SA",
    "SCAR3.SA", "SEER3.SA", "SEQL3.SA", "SHUL4.SA", "SIMH3.SA", "SLCE3.SA", "SMFT3.SA",
    "SMTO3.SA", "SNSY5.SA", "SOJA3.SA", "SOMA3.SA", "STBP3.SA", "SUZB3.SA", "SYNE3.SA",
    "TAEE11.SA", "TAEE3.SA", "TAEE4.SA", "TASA3.SA", "TASA4.SA", "TCSA3.SA", "TECN3.SA",
    "TEND3.SA", "TGMA3.SA", "TKNO4.SA", "TOTS3.SA", "TPIS3.SA", "TRAD3.SA", "TRIS3.SA",
    "TTEN3.SA", "TUPY3.SA", "UCAS3.SA", "UGPA3.SA", "UNIP3.SA", "UNIP5.SA", "UNIP6.SA",
    "USIM3.SA", "USIM5.SA", "VALE3.SA", "VAMO3.SA", "VBBR3.SA", "VIVA3.SA", "VIVR3.SA",
    "VIVT3.SA", "VITT3.SA", "VLID3.SA", "VULC3.SA", "VSTE3.SA", "WEGE3.SA", "WHRL3.SA",
    "WHRL4.SA", "WIZC3.SA", "WLMM3.SA", "WLMM4.SA", "YDUQ3.SA", "ZAMP3.SA" ]
    
    # Baixamos os dados do último dia para todas as ações da lista.
    # É muito mais rápido do que baixar uma por uma.
    dados = yf.download(
        tickers=acoes,
        period="1d",
        progress=False
    )
    
    # O resultado vem com MultiIndex. Acessamos apenas os dados de fechamento ('Close').
    precos_de_fechamento = dados['Close']
    
    # Pegamos a última linha de preços, que corresponde ao fechamento mais recente
    ultimos_precos = precos_de_fechamento.iloc[-1]
    
    # Filtramos a série para manter apenas os preços abaixo do nosso limite
    acoes_filtradas = ultimos_precos[ultimos_precos < PRECO_MAXIMO]
    
    # Removemos ações que possam ter retornado um valor nulo (NaN)
    acoes_filtradas = acoes_filtradas.dropna()

# ===================================================================
# 3. APRESENTAÇÃO DOS RESULTADOS
# ===================================================================

    print("\n\n" + "="*50)
    print("           RESULTADO DO FILTRO DE PREÇO")
    print(f"           Análise do dia: {pd.Timestamp.today().date()}")
    print("="*50)


    if acoes_filtradas.empty:
        print("\nNenhuma ação na lista atendeu ao critério de preço.")
    else:
        print(f"\nEncontradas {len(acoes_filtradas)} ações com preço abaixo de R$ {PRECO_MAXIMO:.2f}:\n")
        # Imprime o resultado formatado
        print(acoes_filtradas.round(2).to_string())
        lista_de_tickers = acoes_filtradas.index.to_list()
        print(lista_de_tickers)

    print("="*50)
    
    return lista_de_tickers