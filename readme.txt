DIDI index
3 8 20 (precos de fechamento de um ativo) -> agulhadas

agulhadas de alta:
media de 3 cruza 8 e 20 para cima

agulhadas de baixa:
media de 3 cruza 8 e 20 para baixo

acima de zero - tendencia de alta
abaixo de zero - tendencia de baixa


ADX
adx mede a forca da tendencia - 0 a 100
valores acima de 25 sugerem uma tendencia forte
abaixo de 20 indicam ausencia de tendencia ou fraca
di+ -> força de tendencia subindo
di- -> força de tendencia descendo

quanto mais alto o adx, mais forte a tendencia
se o di+ > di-, o mercado está com tendencia alta
se di- está acima de di+, o mercado esta com tendencia baixa

TRIX
tres medias moveis
preço do ativo, primeira media movel, segunda media movel
em torno de zero: 
se cruza para cima -> indicativo de compra
quando cruza para baixo -> sinal de venda

ESTOCASTICO LENTO

A linha %K é calculada como uma média móvel da linha %K do estocástico rápido. A linha %D é uma média móvel da linha %K do estocástico lento.

niveis proximos de 80 -> sobrecompra
niveis proximos de 20 -> sobrevenda

cruzamento de linha k sobre linha d podem sinalizar compra
cruzamento de linha k abaixo da linha d pondem sinalizar venda

tendencia alta as linhas k e d tendem a se manter acima de 20
tendencia de baixa as linhas tendem a se manter abaixo de 80

IFR - RSI
de 0 a 100
acima de 70 geralmente indicam sobrecompra (preço alto, possivel queda)
abaixo de 30 indicam sobrevenda (preço baixo, possivel alta)

volume - quantidade de acoes


# Calcular IFR, Estocástico Lento e TRIX
dados.ta.rsi(append=True)
dados.ta.stoch(append=True)
dados.ta.trix(append=True)

# Calcular DI+/DI- (parte do ADX)
dados.ta.adx(append=True)

# Para o Didi Index, o cálculo seria manual:
dados['SMA3'] = dados['Close'].rolling(window=3).mean()
dados['SMA8'] = dados['Close'].rolling(window=8).mean()
dados['SMA20'] = dados['Close'].rolling(window=20).mean()
# A lógica subsequente do Didi Index seria aplicada a estas colunas.

Ate 10 reais
Estocástico lento abaixo de 20 e rsi abaixo de 30 (tambem indicadores de saida)
resultado dia

storm - reversao (media de 9/72 dias comparado a de ontem)


Ate 10 reais
Estocástico lento abaixo de 20 e rsi abaixo de 30 (tambem indicadores de saida)
resultado dia

storm - reversao (media de 9/72 dias comparado a de ontem)



Estratégia de filtragrem - FUNDAMENTALISTA

Etapa 1: Filtros Essenciais (Qualidade e Perfil)
Estes são os filtros não negociáveis para encontrar o tipo certo de empresa.

Liquidez Média Diária

Filtro: Acima de R$ 2.000.000

Por quê? Sua estratégia envolve encontrar pontos de entrada e saída precisos. Uma liquidez saudável garante que você possa executar suas ordens sem dificuldade e com um spread (diferença entre compra e venda) justo.

ROE (Retorno sobre o Patrimônio Líquido)

Filtro: Acima de 15%

Por quê? Este é seu principal filtro de qualidade. Ele garante que você só analise empresas que são altamente eficientes em gerar lucro, o que lhe dá uma segurança fundamental.

P/L (Preço/Lucro)

Filtro: Entre 0 e 20

Por quê? Elimina empresas que dão prejuízo (<0) e aquelas que estão com preços muito "esticados" ou em bolhas de expectativa (>20). Foca em empresas de qualidade a um preço razoável (GARP - Growth at a Reasonable Price).

Valor de Mercado

Filtro: Entre R$ 500 Milhões e R$ 20 Bilhões

Por quê? Foca o scanner em Small e Mid Caps, que, como vimos, tendem a formar as tendências mais claras e ter maior potencial de valorização que a sua estratégia busca capturar.

Etapa 2: Filtros de Cenário Técnico (O "Pulo do Gato")
Aqui está a grande mudança. Em vez de procurar ações que simplesmente caíram, vamos procurar ações que estão em um estado técnico neutro ou "prontas para a ignição".

ADX (14)

Filtro: Acima de 20

Por quê? Este é um pré-filtro genial para a sua estratégia. Ele elimina todas as ações que estão andando de lado, sem tendência nenhuma. Você só vai gastar tempo analisando papéis que já demonstram ter alguma força direcional, seja de alta ou de baixa.

IFR (RSI) (14)

Filtro: Entre 35 e 65

Por quê? Este é o seu filtro "Goldilocks" (Cachinhos Dourados). Você não quer ações extremamente sobrevendidas (<30), pois podem estar em queda livre. E também não quer ações extremamente sobrecompradas (>70), pois sua lógica de compra não funcionaria. Ao buscar ações na faixa intermediária, você encontra papéis que estão "descansando" e prontos para iniciar o próximo movimento, que é o momento ideal para um sinal do seu scanner.
