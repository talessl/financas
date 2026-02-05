import sys
import os
from datetime import date, timedelta
import fundamentus

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infrastructure.factories import criar_provider
from src.domain.use_cases.analisar_acao import AnalisarAcao
from src.infrastructure.providers.yfinance_provider import YFinanceProvider
from src.domain.entities.acoes import Acao

def listar_acoes():
    tickers_df = fundamentus.get_resultado()
    
    # Filtros para análise gráfica (técnica)
    tickers_filtrados = tickers_df[
        (tickers_df['cotacao'] > 0.50) &      # Mínimo R$ 0,50 (evita penny stocks extremas)
        (tickers_df['cotacao'] < 10.0) &      # Abaixo de R$ 10
        (tickers_df['liq2m'] > 5000000)       # Liquidez R$ 5mi+ (ações MOVIMENTADAS)
    ]
    
    # Ordenar por LIQUIDEZ (mais líquidas = mais padrões confiáveis)
    tickers_filtrados = tickers_filtrados.sort_values('liq2m', ascending=False)
    
    print(f"Total de ações filtradas: {len(tickers_filtrados)}")
    print("\nTop 20 mais líquidas abaixo de R$ 10:")
    print(tickers_filtrados[['cotacao', 'liq2m', 'roic', 'roe']].head(20))
    
    tickers = tickers_filtrados.index.tolist()
    tickers_yf = [f"{t}.SA" for t in tickers]
    
    return tickers_yf

def exibir_relatorio(acao: Acao):
    """
    Função simples atuando como 'View' para formatar a saída
    """
    print("\n" + "="*40)
    print(f" RELATÓRIO: {acao.ticker}")
    print("="*40)
    
    if not acao.historico:
        print("Sem dados históricos disponíveis.")
        return

    # Usando métodos da Entidade (Regra de Negócio)
    preco_atual = acao.historico[-1].close
    maxima = acao.obter_maxima_historica()
    minima = acao.obter_minima_historica()

    print(f"Periodo Analisado: {len(acao.historico)} dias")
    print(f"Preço Atual:      R$ {preco_atual:.2f}")
    print(f"Maxima do Periodo: R$ {maxima:.2f}")
    print(f"Minima do Periodo: R$ {minima:.2f}")
    
    print("Ultimos 5 registros:")
    print(f"{'Data':<12} | {'Fechamento':<10} | {'Alta':<10} | {'Baixa':<10}")
    print("-" * 50)
    
    for dado in acao.historico[-5:]:
        data_fmt = dado.data.strftime('%d/%m/%Y')
        print(f"{data_fmt:<12} | R$ {dado.close:<7.2f} | R$ {dado.high:<7.2f} | R$ {dado.low:<7.2f}")
    print("="*40 + "\n")


def main():
    ticker = "DASA3.SA"
    
    meu_provider = criar_provider()
    
    use_case = AnalisarAcao(provider=meu_provider)
    
    print(f"--- Analisando {ticker} ---")
    # acao = use_case.buscar(ticker)
    
    # if acao:
    #     exibir_relatorio(acao)
        
    acoes_baixas = listar_acoes()
    adx = use_case.filtrar_adx(acoes_baratas=acoes_baixas)
    rsi = use_case.filtrar_rsi(acoes_baratas=acoes_baixas)
    print(adx)
    print(rsi)
    print(list(set(adx) & set(rsi)))
    
if __name__ == "__main__":
    main()