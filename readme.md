# Dashboard Financeiro: Home Broker B3

Aplicação web para análise de ações da B3. Busca o histórico de preços, calcula indicadores técnicos e varre o mercado em busca de ativos em sobrevenda.

**Stack:** Python, FastAPI, Jinja2, Fundamentus (dados de mercado) e pandas-ta (indicadores).

## Funcionalidades

- **Busca de ações:** mostra preço atual, máxima e mínima dos últimos 30 dias. Não precisa de formatação: para `DASA3`, digite `dasa3`.
- **Visualizar Ações do Dia (scanner):** aplica a estratégia abaixo a todas as ações da B3 e lista as que passam no filtro.

## Como executar

1. Crie e ative o ambiente virtual:

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Linux/macOS
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Na raiz do projeto (`financas`), inicie o servidor:

   ```bash
   uvicorn src.infrastructure.web.main:app --reload
   ```

4. Acesse `http://127.0.0.1:8000` no navegador.

## Estratégia do scanner

Procura ações em **sobrevenda**, com preço abaixo de R$ 10:

- Estocástico Lento **< 20**
- IFR (RSI) **< 30**

São necessários pelo menos 30 períodos de histórico para calcular os indicadores.

## Indicadores

| Indicador | O que mede | Como ler |
| --- | --- | --- |
| **IFR (RSI)** | Velocidade das variações de preço (0 a 100) | Acima de 70: sobrecompra. Abaixo de 30: sobrevenda. |
| **Estocástico Lento** | Posição do fechamento dentro da faixa recente (linhas %K e %D) | Acima de 80: sobrecompra. Abaixo de 20: sobrevenda. Cruzamento de %K sobre %D indica compra ou venda. |
| **DIDI Index** | Médias móveis de 3, 8 e 20 períodos | "Agulhada": a média de 3 cruza as outras duas, para cima (alta) ou para baixo (baixa). |
| **ADX** | Força da tendência (0 a 100), sem indicar a direção | Abaixo de 20: sem tendência. Acima de 25: tendência forte. `DI+` acima de `DI-` indica alta. |
| **TRIX** | Momentum filtrado por três médias exponenciais | Cruza o zero para cima: compra. Para baixo: venda. |
| **Volume** | Quantidade negociada | Confirma a força do movimento de preço. |

## Próximos passos

- Filtros fundamentalistas para o scanner (perfil GARP: crescimento a preço razoável).
- Melhorias na experiência de consulta das ações.
