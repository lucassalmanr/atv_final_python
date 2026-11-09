# Conferência do enunciado — Grupo 5

| Pedido | Situação |
|---|---|
| Pasta atividade_final e planilha dentro dela | Atendido |
| requirements.txt com streamlit, pandas, plotly e python-calamine | Atendido |
| Leitura da planilha e comparação por raça | Atendido |
| KPI da mediana por transporte e raça | Atendido; mediana entre municípios com dados, com cobertura explícita |
| Público versus particular versus ativo | Atendido com categorias disponíveis; táxi e mototáxi incluídos no individual |
| Cidades com maior uso de bicicleta | Atendido; ranking por raça, empates, CSV e comparação das cidades do cenário |
| Filtro UF | Atendido |
| Filtro de meio de transporte | Atendido para KPIs e boxplot; rosca mantém a distribuição completa |
| Filtro por região metropolitana | Não atendido literalmente: a tabela não delimita regiões metropolitanas |
| Filtro por renda | Não atendido: variável ausente; controle indica indisponibilidade |
| Boxplot de tempo de deslocamento e gargalos | Não atendido: variável ausente; gráfico complementar de percentuais explicitamente identificado |
| Pizza/rosca | Atendido para distribuições completas |
| Conteúdo de caos no trânsito e mobilidade sustentável | Atendido: dois resumos com fontes e datas |
| Fotos de vias e transporte público | Atendido: duas fotos locais com créditos |
| Roda de conversa como startup | Roteiro e clientes fictícios no LEIA_ME.md |
| Deploy obrigatório | Pendente: requer repositório e conta de publicação; instruções incluídas |

O projeto não deve ser declarado como cumprimento integral do enunciado: faltam variáveis na fonte e a publicação efetiva. Uma base complementar precisa conter tempo, renda e delimitação metropolitana compatíveis para cobrir os requisitos ausentes; inserir números fictícios produziria conclusões incorretas.

## Verificação executada

Leitura da planilha, identificação de municípios, ausência de chaves duplicadas, percentuais válidos, somas nacionais por categoria comparadas com valores conhecidos, integridade das imagens e execução do painel com AppTest do Streamlit. Foram exercitados os filtros das UFs do cenário, os seis transportes, as três raças, uma distribuição com valores ausentes e o retorno à distribuição nacional.

Essa verificação cobre execução e resultados programáticos. Não equivale a uma publicação no Streamlit Cloud ou uma inspeção visual em todos os dispositivos.
