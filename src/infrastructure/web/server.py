import sys
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Truque para o Python achar a pasta src (igual fizemos no console)
sys.path.append(os.getcwd())

# Imports da Clean Architecture
from src.domain.use_cases.analisar_acao import AnalisarAcao

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/infrastructure/web/static"), name="static")


# Configurando onde estão os HTMLs
from src.infrastructure.factories import criar_provider
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

        # Prepara os dados para a View (Poderia ser um ViewModel aqui!)
        maxima = acao.obter_maxima_historica()
        minima = acao.obter_minima_historica()
        
        datas_grafico = [dado.data.strftime("%d/%m") for dado in acao.historico]
        precos_grafico = [dado.close for dado in acao.historico]

        return templates.TemplateResponse("index.html", {
            "request": request,
            "acao": acao,
            "maxima": maxima,
            "minima": minima,
            "datas_grafico": datas_grafico,   # Enviando as datas
            "precos_grafico": precos_grafico  # Enviando os preços
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Erro interno: {str(e)}"
        })

# Para rodar direto pelo arquivo (opcional)
if __name__ == "__main__":
    import uvicorn
    # Roda o servidor na porta 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)