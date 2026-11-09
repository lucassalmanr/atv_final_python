# Grupo 5 — Transporte e mobilidade urbana

## Executar

Abra o terminal dentro da pasta atividade_final e execute:

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## Apresentação

O grupo representa uma startup de análise de dados em uma roda de conversa. Os clientes fictícios são Fernando (mobilidade nacional), Ana (região metropolitana de Goiânia), Luciene (Vitória), Pedrinho (Belo Horizonte) e Lucas (Brasília).

Apresente primeiro o universo: mulheres de 10 anos ou mais, ocupadas na semana de referência, por cor ou raça, em 2022. A tabela informa o meio em que passam mais tempo no deslocamento ao trabalho principal.

1. Mostre os cartões de mediana por raça (KPIs).
2. Explique a rosca e compare coletivo, carro/moto e ativo.
3. Mostre o ranking de bicicleta e as quatro cidades do cenário.
4. Relacione as notícias à mobilidade urbana e explique os limites da tabela.

## Respostas principais

KPI significa indicador-chave de desempenho: é o número em destaque que resume a análise. O pedido do enunciado é destacar a mediana por transporte e raça. O cálculo aqui usa municípios, sem misturar totais de Brasil, regiões e estados. O painel permite consultar todos os modais e a cobertura dos cálculos.

Para transporte coletivo, as medianas municipais, considerando apenas números disponíveis, são 8,10% para brancas, 9,40% para pretas ou pardas e 41,50% para indígenas. A cobertura é de 4.932, 5.290 e 625 municípios, respectivamente. A comparação exige cautela: as medianas são condicionadas à presença de valores numéricos e não são percentuais nacionais.

Na linha Brasil da planilha:

| Categoria | Brancas | Pretas ou pardas | Indígenas |
|---|---:|---:|---:|
| Coletivo | 25,2% | 34,6% | 22,4% |
| Carro/táxi + moto/mototáxi | 51,7% | 34,8% | 30,6% |
| Ativo: a pé + bicicleta | 22,6% | 30,0% | 43,4% |
| Outros | 0,5% | 0,6% | 3,6% |

A categoria individual inclui táxi e mototáxi. O coletivo não separa ônibus de metrô. Não há totais por raça para calcular um percentual consolidado por média ponderada.

Entre as quatro cidades do cenário, Vitória tem o maior percentual de bicicleta nos três grupos: 2,7% entre brancas, 3,9% entre pretas ou pardas e 15,1% entre indígenas. No ranking de todos os municípios, as líderes são Novo Santo Antônio (MT), com 94,1% entre brancas, e Morrinhos do Sul (RS), com 100% entre pretas ou pardas. Entre indígenas há vários municípios empatados em 100%, listados no painel. Esses percentuais não representam todos os moradores nem indicam o número absoluto de ciclistas.

## Limitações e metodologia

- Ano disponível: 2022. Não representa uma série histórica.
- Símbolos não numéricos são tratados como indisponíveis; o arquivo enviado não traz legenda para interpretá-los como zero. Os KPIs exibem quantos municípios entraram no cálculo.
- Cada mediana é independente. Não some as medianas dos modais nem as porcentagens de grupos raciais diferentes.
- Uma rosca com categorias sem valor numérico é omitida, evitando apresentar uma composição parcial como total.
- A UF filtra os municípios usados nos KPIs, boxplot e ranking. O seletor de local da rosca é independente e inclui totais publicados. Essa diferença é rotulada no painel.
- A planilha não traz tempo de viagem, renda ou delimitações metropolitanas. Esses requisitos não podem ser cumpridos literalmente com a fonte fornecida. O boxplot complementar é de percentuais, com aviso explícito; não mede minutos nem gargalos.

## Deploy obrigatório — etapa pendente na sua conta

O projeto está organizado para Streamlit Community Cloud, mas não foi publicado.

1. Envie toda a pasta para um repositório no GitHub.
2. Entre em https://share.streamlit.io com a conta vinculada ao GitHub.
3. Escolha Create app e selecione repositório e branch.
4. Use app.py como arquivo principal se os arquivos estiverem na raiz; use atividade_final/app.py se a pasta estiver dentro do repositório.
5. Clique em Deploy e abra o endereço gerado.

Documentação oficial: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

As notícias e imagens têm fonte e crédito no painel e no arquivo noticias.json. Os textos são resumos próprios.
