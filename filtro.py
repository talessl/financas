import yfinance as yf
import pandas_ta as ta

def verificar_rsi_sobrevenda(ticker: str, limite_rsi: int = 35)->bool:
    try:
        dados = yf.download(ticker, period="6mo", progress=False, auto_adjust=True)
        dados.columns = dados.columns.droplevel(1)

        dados.ta.rsi(append=True)
        ultimo_rsi = dados['RSI_14'].dropna().iloc[-1]
        return ultimo_rsi < limite_rsi
    except Exception as e:
            print(f"Ocorreu um erro ao processar {ticker}: {e}")
            return False


def verificar_stoch_sobrevenda(ticker: str, limite_stoch: int = 25)-> bool:
    try:

        dados = yf.download(ticker, period="6mo", progress=False, auto_adjust=True)
        dados.columns = dados.columns.droplevel(1)

        dados.ta.stoch(append=True)

        ultimo_stoch = dados['STOCHk_14_3_3'].dropna().iloc[-1]
        return ultimo_stoch < limite_stoch

    except Exception as e:
                print(f"Ocorreu um erro ao processar {ticker}: {e}")
                return False

def filtro_duplo(ticker: str) -> bool:
    if (verificar_rsi_sobrevenda(ticker) and verificar_rsi_sobrevenda(ticker)):
        return True

def filtragem(lista_acoes: str) -> str:
    resultado = []
    for acao in lista_acoes:
        if filtro_duplo(acao):
            resultado.append(acao)
    return resultado

acoes_hoje = ['AALR3.SA', 'AERI3.SA', 'AGXY3.SA', 'ALLD3.SA', 'ALPA4.SA', 'ALPK3.SA', 'ALUP4.SA', 'AMAR3.SA', 'AMER3.SA', 'ANIM3.SA', 'ARML3.SA', 'ATED3.SA', 'AURE3.SA', 'AVLL3.SA', 'AZEV3.SA', 'AZEV4.SA', 'AZUL4.SA', 'BEEF3.SA', 'BEES3.SA', 'BEES4.SA', 'BHIA3.SA', 'BIOM3.SA', 'BMGB4.SA', 'BOBR4.SA', 'BPAC5.SA', 'BPAN4.SA', 'BRKM3.SA', 'BRKM5.SA', 'BSLI3.SA', 'BSLI4.SA', 'CAML3.SA', 'CASH3.SA', 'CBAV3.SA', 'CEED3.SA', 'CMIN3.SA', 'COGN3.SA', 'CSAN3.SA', 'CSED3.SA', 'CSNA3.SA', 'CVCB3.SA', 'DASA3.SA', 'DESK3.SA', 'DEXP3.SA', 'DEXP4.SA', 'DOHL4.SA', 'DOTZ3.SA', 'DTCY3.SA', 'DXCO3.SA', 'ECOR3.SA', 'ENGI4.SA', 'ENJU3.SA', 'EPAR3.SA', 'ESPA3.SA', 'ETER3.SA', 'EVEN3.SA', 'FESA4.SA', 'FHER3.SA', 'FIQE3.SA', 'GMAT3.SA', 'GOAU3.SA', 'GOAU4.SA', 'GRND3.SA', 'GSHP3.SA', 'GUAR3.SA', 'HAGA3.SA', 'HAGA4.SA', 'HBRE3.SA', 'HBSA3.SA', 'HOOT4.SA', 'INEP3.SA', 'INEP4.SA', 'JALL3.SA', 'JFEN3.SA', 'JHSF3.SA', 'KEPL3.SA', 'KLBN3.SA', 'KLBN4.SA', 'LIGT3.SA', 'LJQQ3.SA', 'LPSB3.SA', 'LUPA3.SA', 'LUXM4.SA', 'LVTC3.SA', 'LWSA3.SA', 'MAPT4.SA', 'MATD3.SA', 'MEAL3.SA', 'MELK3.SA', 'MGEL4.SA', 'MGLU3.SA', 'MLAS3.SA', 'MRVE3.SA', 'NEXP3.SA', 'NUTR3.SA', 'OIBR3.SA', 'OIBR4.SA', 'ONCO3.SA', 'OPCT3.SA', 'OSXB3.SA', 'PCAR3.SA', 'PDTC3.SA', 'PETZ3.SA', 'PFRM3.SA', 'PGMN3.SA', 'PINE3.SA', 'PINE4.SA', 'PNVL3.SA', 'POMO3.SA', 'POMO4.SA', 'POSI3.SA', 'PTBL3.SA', 'PTNT3.SA', 'PTNT4.SA', 'QUAL3.SA', 'RAIZ4.SA', 'RANI3.SA', 'RAPT3.SA', 'RAPT4.SA', 'RCSL3.SA', 'RCSL4.SA', 'RDNI3.SA', 'REDE3.SA', 'RNEW11.SA', 'RNEW3.SA', 'RNEW4.SA', 'ROMI3.SA', 'RPMG3.SA', 'RSID3.SA', 'SAPR3.SA', 'SAPR4.SA', 'SEER3.SA', 'SEQL3.SA', 'SHUL4.SA', 'SIMH3.SA', 'SNSY5.SA', 'SYNE3.SA', 'TASA3.SA', 'TASA4.SA', 'TCSA3.SA', 'TECN3.SA', 'TPIS3.SA', 'TRAD3.SA', 'TRIS3.SA', 'UCAS3.SA', 'USIM3.SA', 'USIM5.SA', 'VAMO3.SA', 'VITT3.SA', 'VIVR3.SA', 'VSTE3.SA', 'WHRL3.SA', 'WHRL4.SA', 'WIZC3.SA', 'ZAMP3.SA']

print(filtragem(acoes_hoje))
