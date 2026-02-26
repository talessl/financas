# Livro de Estratégias e Indicadores de Análise Técnica

Este documento centraliza as definições de indicadores técnicos e os códigos para implementação.

## 1. Definições de Indicadores Técnicos

Uma referência rápida sobre os principais indicadores utilizados.

### DIDI Index

- **Composição:** Baseado nos preços de fechamento de um ativo, utilizando médias móveis de 3, 8 e 20 períodos.
- **Conceito Principal:** Identificação de "agulhadas", que são cruzamentos específicos das médias.
- **Sinais:**
  - **Agulhada de Alta (Compra):** A média de 3 cruza as médias de 8 e 20 para cima.
  - **Agulhada de Baixa (Venda):** A média de 3 cruza as médias de 8 e 20 para baixo.
- **Contexto de Tendência:**
  - **Acima de zero:** Sugere tendência de alta.
  - **Abaixo de zero:** Sugere tendência de baixa.

### ADX (Average Directional Index)

- **Função:** Mede a **força** da tendência, numa escala de 0 a 100 (não indica a direção).
- **Interpretação da Força:**
  - **Abaixo de 20:** Ausência de tendência ou tendência fraca.
  - **Acima de 25:** Sugere uma tendência forte.
- **Componentes (Direção):**
  - `DI+`: Mede a força da tendência de alta.
  - `DI-`: Mede a força da tendência de baixa.
- **Análise Combinada:**
  - Quanto mais alto o ADX, mais forte é a tendência (seja ela de alta ou baixa).
  - Se `DI+` está acima de `DI-`, o mercado está em tendência de alta.
  - Se `DI-` está acima de `DI+`, o mercado está em tendência de baixa.

### TRIX (Triple Exponential Average)

- **Composição:** Baseado em três médias móveis exponenciais.
- **Função:** Oscilador de momentum que filtra ruídos do mercado.
- **Sinais (Cruzamento de Zero):**
  - **Sinal de Compra:** Quando o TRIX cruza a linha zero para cima.
  - **Sinal de Venda:** Quando o TRIX cruza a linha zero para baixo.

### Estocástico Lento

- **Composição:** Composto por duas linhas:
  - **%K:** Média móvel da linha %K do estocástico rápido.
  - **%D:** Média móvel da linha %K (lenta).
- **Zonas de Interesse:**
  - **Sobrecompra:** Níveis próximos ou acima de 80.
  - **Sobrevenda:** Níveis próximos ou abaixo de 20.
- **Sinais de Cruzamento:**
  - **Sinal de Compra:** Linha %K cruza a linha %D para cima (especialmente saindo da zona de sobrevenda).
  - **Sinal de Venda:** Linha %K cruza a linha %D para baixo (especialmente saindo da zona de sobrecompra).
- **Contexto de Tendência:**
  - **Tendência de Alta:** As linhas %K e %D tendem a se manter acima do nível 20.
  - **Tendência de Baixa:** As linhas %K e %D tendem a se manter abaixo do nível 80.

### IFR (RSI - Índice de Força Relativa)

- **Função:** Oscilador de momentum que mede a velocidade e a mudança dos movimentos de preços, numa escala de 0 a 100.
- **Zonas de Interesse:**
  - **Sobrecompra:** Níveis acima de 70 (sugere que o preço está alto, possível reversão para queda).
  - **Sobrevenda:** Níveis abaixo de 30 (sugere que o preço está baixo, possível reversão para alta).

### Volume

- **Função:** Mede a quantidade de ações ou contratos negociados em um período. Confirma a força de um movimento de preço.

---

## 2. Estratégia de Rastreamento (Scanner)

Combinação de filtros fundamentalistas e técnicos para encontrar ações com potencial.

### Etapa 1: Filtros Essenciais (Qualidade e Perfil)

Filtros não negociáveis para encontrar o tipo certo de empresa (GARP - Growth at a Reasonable Price).

### Etapa 2: Filtros de Cenário Técnico (Timing)

Filtros para encontrar ações que estão em um estado técnico neutro ou "prontas para a ignição". Necessário ao menos 30 períodos.

#### ADX (14)

- **Filtro:** Acima de 20
  > **Por quê?** Elimina ações que estão "andando de lado" (sem tendência). Foca a análise apenas em papéis que já demonstram força direcional.

#### IFR (RSI) (14)

- **Filtro:** Entre 35 e 65
  > **Por quê?** Filtro "Goldilocks". Evita ações extremamente sobrevendidas (<30, podem estar em queda livre) ou sobrecompradas (>70). Busca papéis que estão "descansando" e prontos para o próximo movimento.
