from src.domain.provider_interface import IDataProvider
from src.domain.entities.acoes import Acao
from datetime import date, timedelta

class AnalisarAcao:
    # AQUI acontece a Mágica da Injeção de Dependência.
    def __init__(self, provider: IDataProvider):
        self.provider = provider
        
    def buscar(self, ticker: str):
        hoje = date.today()
        inicio = hoje - timedelta(days=45)
        
        dados = self.provider.buscar_dados(ticker, inicio, hoje)
        if not dados: 
            return None
        
        return Acao(ticker=ticker, historico=dados)
    
    def filtrar_adx(self, acoes_baratas):
        inicio = date.today() - timedelta(days=60) 
        fim = date.today()
        
        print(f"[DEBUG] Filtrando {len(acoes_baratas[:20])} ações")
        print(f"[DEBUG] Período: {inicio} até {fim}")
        print(f"[DEBUG] Primeiras ações: {acoes_baratas[:5]}")
        
        dados = self.provider.filtrar_adx(
            tickers=acoes_baratas[:20],
            inicio=inicio,
            fim=fim,
            periodo=14,
            limite=20.0
        )
        
        print(f"[DEBUG] Tipo do retorno: {type(dados)}")
        print(f"[DEBUG] Valor do retorno: {dados}")
        print(f"[DEBUG] Tamanho: {len(dados) if dados else 'None ou vazio'}")
        
        if not dados:  # Verifica se é None, [] ou vazio
            print("[DEBUG] Nenhuma ação passou no filtro ADX!")
            return None
        
        print(f"[DEBUG] {len(dados)} ações aprovadas: {dados}")
        return dados

    def filtrar_rsi(self, acoes_baratas):
        inicio = date.today() - timedelta(days=60) 
        fim = date.today()
        
        dados = self.provider.filtrar_rsi(
            tickers=acoes_baratas[:20],
            inicio=inicio,
            fim=fim,
            periodo=14,
            limite_min=35.0,
            limite_max=65.0
        )

    
        if not dados:  # Verifica se é None, [] ou vazio
                print("[DEBUG] Nenhuma ação passou no filtro ADX!")
                return None
            
        print(f"[DEBUG] {len(dados)} ações aprovadas: {dados}")
        return dados