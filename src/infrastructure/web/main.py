from src.infrastructure.factories import criar_provider
from src.domain.use_cases.analisar_acao import AnalisarAcao
import sys
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import fundamentus
from datetime import datetime, timedelta

SCANNER_CACHE = {
    "dados": None,
    "expira_em": None
}

# Truque para o Python achar a pasta src (igual fizemos no console)
sys.path.append(os.getcwd())

# Imports da Clean Architecture

app = FastAPI()

app.mount(
    "/static", StaticFiles(directory="src/infrastructure/web/static"), name="static")


# Configurando onde estão os HTMLs
templates = Jinja2Templates(directory="src/infrastructure/web/templates")

# --- FÁBRICA DE DEPENDÊNCIAS ---


def get_use_case():
    provider = criar_provider()
    return AnalisarAcao(provider)

# --- ROTAS (CONTROLLERS) ---


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Renderiza a página inicial"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/acoes", response_class=HTMLResponse)
async def home(request: Request):
    """Renderiza a página inicial"""
    return templates.TemplateResponse("acoes.html", {"request": request})


@app.get("/buscar_acoes", response_class=HTMLResponse)
async def buscar_acoes(request: Request):
    """Rota que executa o Scanner com Cache de Performance"""
    use_case = get_use_case()
    agora = datetime.now()

    if SCANNER_CACHE["dados"] and SCANNER_CACHE["expira_em"] and SCANNER_CACHE["expira_em"] > agora:
        print("🚀 Retornando dados instantaneamente do CACHE!")
        return templates.TemplateResponse("acoes.html", {
            "request": request,
            "lista_acoes": SCANNER_CACHE["dados"]
        })

    try:
        print("⏳ Cache vazio ou expirado. Iniciando busca na B3 e YFinance...")

        df_b3 = fundamentus.get_resultado()
        df_baratas = df_b3[
            (df_b3['cotacao'] > 0) &
            (df_b3['cotacao'] <= 10.0) &
            (df_b3['liq2m'] > 1000000)
        ]

        tickers_para_escanear = [f"{ticker}.SA" for ticker in df_baratas.index]

        acoes_filtradas = use_case.escanear_oportunidades(
            tickers=tickers_para_escanear, preco_maximo=10.0)

        SCANNER_CACHE["dados"] = acoes_filtradas
        SCANNER_CACHE["expira_em"] = agora + timedelta(minutes=15)
        print(
            f"✅ Cache atualizado! Próxima busca real só a partir de: {SCANNER_CACHE['expira_em'].strftime('%H:%M:%S')}")

        return templates.TemplateResponse("acoes.html", {
            "request": request,
            "lista_acoes": acoes_filtradas
        })

    except Exception as e:
        return templates.TemplateResponse("acoes.html", {
            "request": request,
            "error": f"Erro ao executar o scanner dinâmico: {str(e)}"
        })


@app.post("/analisar", response_class=HTMLResponse)
async def analisar(request: Request, ticker: str = Form(...)):
    """
    Recebe o formulário, chama o Use Case e devolve o HTML preenchido.
    Isso é o fluxo: Web -> Controller -> Use Case -> Web
    """
    use_case = get_use_case()

    try:
        # Chama a Regra de Negócio (Nível Alto)
        # Note que o Use Case nem sabe que foi chamado via Web
        final_ticker = ticker if ticker.upper().endswith('.SA') else ticker + '.SA'
        acao = use_case.buscar(final_ticker)

        if not acao:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": f"Não foi possível encontrar dados para {ticker}"
            })

        maxima = acao.obter_maxima_historica()
        minima = acao.obter_minima_historica()
        datas_grafico = [dado.data.strftime(
            "%d/%m") for dado in acao.historico]
        precos_grafico = [dado.close for dado in acao.historico]

        # Pede ao Domínio que calcule os indicadores estruturados
        rsi_grafico = acao.calcular_rsi()
        stoch_k, stoch_d = acao.calcular_estocastico()
        didi_curta, didi_longa = acao.calcular_didi_index()

        return templates.TemplateResponse("index.html", {
            "request": request,
            "acao": acao,
            "maxima": maxima,
            "minima": minima,
            "datas_grafico": datas_grafico,
            "precos_grafico": precos_grafico,
            # Passando as métricas isoladas para o Template Jinja
            "rsi_grafico": rsi_grafico,
            "stoch_k_grafico": stoch_k,
            "stoch_d_grafico": stoch_d,
            "didi_curta_grafico": didi_curta,
            "didi_longa_grafico": didi_longa
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Erro interno: {str(e)}"
        })

# Para rodar direto pelo arquivo (opcional)
if __name__ == "__main__":
    import uvicorn
    # Roda o servidor na porta 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
