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
