"""Dashboard da Tabela 13 (2022): transporte e mobilidade urbana."""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from dados import MODAIS, RACAS, agrupar, carregar


# -----------------------------------------------------------------------------
# Configuração e funções auxiliares
# -----------------------------------------------------------------------------

st.set_page_config(page_title="Mobilidade • Grupo 5", layout="wide")


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    """Carrega a base uma vez por sessão para evitar leituras repetidas."""
    return carregar()


def formatar_percentual(valor: float | None) -> str:
    """Converte um percentual para o padrão brasileiro ou indica falta de dado."""
    return "Sem dados" if valor is None or pd.isna(valor) else f"{valor:.2f}%".replace(".", ",")


def criar_grafico_rosca(dados: pd.DataFrame):
    """Monta o gráfico de participação dos meios de transporte."""
    fig = px.pie(dados, names="Transporte", values="Percentual", hole=0.5,
                 category_orders={"Transporte": MODAIS})
    fig.update_traces(texttemplate="%{value:.1f}%",
                      hovertemplate="%{label}: %{value:.1f}%<extra></extra>")
    return fig


# -----------------------------------------------------------------------------
# Cabeçalho, base e filtros globais
# -----------------------------------------------------------------------------

st.title("Transporte e mobilidade urbana das mulheres")
st.caption("Grupo 5 • Tabela 13 • 2022")
st.write(
    "Análise do meio de transporte em que mulheres de 10 anos ou mais, ocupadas "
    "na semana de referência, passam mais tempo no deslocamento ao trabalho "
    "principal, por cor ou raça."
)

base = carregar_dados()

# Keep only Brazil and the four cities defined for this project.  Prefixes are
# used because some accented characters in the source spreadsheet are damaged.
nomes_locais = base["Local"].fillna("")
eh_brasil = nomes_locais.eq("Brasil")
eh_cidade_cenario = (
    (base["UF"].eq("GO") & nomes_locais.str.fullmatch(r"Goi.nia \(GO\)"))
    | (base["UF"].eq("ES") & nomes_locais.str.fullmatch(r"Vit.ria \(ES\)"))
    | (base["UF"].eq("MG") & nomes_locais.str.startswith("Belo Horizonte"))
    | (base["UF"].eq("DF") & nomes_locais.str.fullmatch(r"Bras.lia \(DF\)"))
)
base = base[eh_brasil | eh_cidade_cenario].copy()

# Linhas com UF correspondem a municípios; as demais são agregados da base.
municipios = base[base["UF"].notna()]

uf = st.sidebar.selectbox("UF dos municípios", ["Todas", *sorted(municipios["UF"].unique())], key="uf")
modal = st.sidebar.selectbox("Meio de transporte", MODAIS, index=4, key="modal")
raca = st.sidebar.selectbox("Cor ou raça da rosca e do ranking", RACAS, key="raca")

# O filtro de UF é usado apenas nas análises municipais.
recorte = base[base["Local"].eq("Brasil")] if uf == "Todas" else municipios[municipios["UF"] == uf]


# -----------------------------------------------------------------------------
# 1. Medianas municipais por modal e raça
# -----------------------------------------------------------------------------

st.subheader("1. Mediana por meio de transporte e raça")
st.write(f"Transporte: **{modal}** · Municípios: **{uf}**")

if uf == "Todas":
    st.caption("Selecao atual: Brasil (dado nacional agregado).")

selecao = recorte[recorte["Transporte"] == modal]

# Os cartões usam somente valores numéricos de cada grupo racial.
for coluna, grupo in zip(st.columns(3), RACAS):
    valores = selecao.loc[selecao["Cor ou raça"] == grupo, "Percentual"].dropna()
    coluna.metric(grupo, formatar_percentual(valores.median() if not valores.empty else None))
    coluna.caption(f"{len(valores)} municípios com valor numérico")

st.caption("KPI é o indicador destacado no cartão. Aqui, usamos a mediana dos percentuais municipais. Cada município tem o mesmo peso; o resultado não é o percentual nacional. Células sem número não viram zero.")

# -----------------------------------------------------------------------------
# 2. Distribuição por categoria de mobilidade
# -----------------------------------------------------------------------------

st.subheader("2. Participação do coletivo, individual e ativo")

# A distribuicao usa exatamente o mesmo recorte escolhido no cabecalho.
# "Todas" representa Brasil; cada UF representa sua unica cidade no cenario.
local = "Brasil" if uf == "Todas" else municipios.loc[municipios["UF"] == uf, "Local"].iat[0]

trecho = base[(base["Local"] == local) & (base["Cor ou raça"] == raca)]
st.write(f"**{local} • {raca}**")

# A rosca é omitida quando a composição não é completa, para não sugerir 100%.
if trecho["Percentual"].isna().any():
    st.warning("A distribuição possui categorias sem valor numérico. A rosca foi omitida para não apresentar uma composição incompleta como 100%.")
else:
    st.plotly_chart(criar_grafico_rosca(trecho), width="stretch")
    lider = trecho.loc[trecho["Percentual"].idxmax()]
    st.write(f"Maior participação: **{lider.Transporte} — {lider.Percentual:.1f}%**.")
    st.caption("Rótulos mostram valores originais. Arredondamentos podem gerar somas ligeiramente diferentes de 100%. O filtro de transporte não corta fatias da rosca.")

st.caption("Coletivo não separa ônibus e metrô. O agrupamento individual inclui táxi e mototáxi, portanto não mede apenas veículos particulares. Não há totais populacionais para consolidar raças por média ponderada.")


# -----------------------------------------------------------------------------
# 3. Ranking de uso de bicicleta
# -----------------------------------------------------------------------------

st.subheader("3. Uso de bicicleta: Brasil e quatro cidades")

# Esta comparação é fixa e não depende dos filtros do cabeçalho.
# A base já foi limitada a Brasil, Goiânia, Vitória, Belo Horizonte e Brasília.
bikes = (
    base[base["Transporte"] == "Bicicleta"]
    .dropna(subset=["Percentual"])
    .sort_values(["Local", "Cor ou raça"])
)

if bikes.empty:
    st.info("Sem valores numéricos para a comparação.")
else:
    fig = px.bar(
        bikes,
        x="Percentual",
        y="Local",
        color="Cor ou raça",
        orientation="h",
        barmode="group",
        text="Percentual",
        category_orders={"Cor ou raça": RACAS},
    )
    fig.update_layout(yaxis_title="", xaxis_title="Uso de bicicleta (%)", legend_title="Cor ou raça")
    st.plotly_chart(fig, width="stretch")

    lideres = bikes[bikes["Percentual"] == bikes["Percentual"].max()]
    st.write(f"Maior percentual: **{bikes['Percentual'].max():.1f}%**. Há **{len(lideres)}** local(is) com esse valor.")
    st.download_button("Baixar dados do gráfico", bikes[["Local", "Cor ou raça", "Percentual"]].to_csv(index=False).encode("utf-8-sig"), "bicicleta_cenario.csv", "text/csv")

st.caption("O gráfico mostra os três grupos raciais em cada local e não é alterado pelos filtros do cabeçalho. O percentual é interno a cada grupo racial, não representa o número de ciclistas.")

# -----------------------------------------------------------------------------
# 4. Perfil de mobilidade por categoria
# -----------------------------------------------------------------------------

st.subheader("4. Transporte público, particular e ativo")
st.write(f"**{local} • {raca}**")

# Agrupa os seis meios de transporte nas categorias solicitadas pela pergunta.
categorias_mobilidade = agrupar(trecho).copy()
categorias_mobilidade["Categoria"] = [
    "Transporte público",
    "Transporte particular",
    "Mobilidade ativa",
    "Outros",
]

if categorias_mobilidade["Percentual"].isna().any():
    st.info("Não há dados completos para montar a composição por categoria.")
else:
    fig = px.pie(
        categorias_mobilidade,
        names="Categoria",
        values="Percentual",
        hole=0.5,
        category_orders={
            "Categoria": [
                "Transporte público",
                "Transporte particular",
                "Mobilidade ativa",
                "Outros",
            ]
        },
    )
    fig.update_traces(
        texttemplate="%{label}<br>%{value:.1f}%",
        hovertemplate="%{label}: %{value:.1f}%<extra></extra>",
    )
    st.plotly_chart(fig, width="stretch")

st.caption("O gráfico inclui “Outros” para que a composição fique completa. A base representa mulheres ocupadas de 10 anos ou mais, não toda a população.")

# -----------------------------------------------------------------------------
# 5. Distribuição dos percentuais municipais
# -----------------------------------------------------------------------------

st.subheader("5. Boxplot: distribuição municipal por cor ou raça")
st.write("O gráfico compara Brasil, Goiânia, Vitória, Belo Horizonte e Brasília para o meio de transporte selecionado.")

# Comparação fixa: Brasil e as quatro cidades, independentemente da UF escolhida.
validos = base[base["Transporte"] == modal].dropna(subset=["Percentual"])
if validos.empty:
    st.info("Sem dados para o boxplot.")
else:
    fig = px.box(validos, x="Cor ou raça", y="Percentual", color="Cor ou raça", hover_data=["Local"], points="outliers", category_orders={"Cor ou raça": RACAS})
    fig.update_traces(quartilemethod="linear")
    fig.update_layout(showlegend=False, yaxis_title="Percentual municipal (%)")
    st.plotly_chart(fig, width="stretch")

st.caption("Linha interna: mediana. Caixa: 50% centrais. Bigodes: valores dentro de 1,5 vez o intervalo interquartil a partir dos quartis. Pontos externos: outliers. Eles não demonstram congestionamento.")


# -----------------------------------------------------------------------------
# 6. Reportagem de contexto
# -----------------------------------------------------------------------------

st.subheader("6. Mobilidade urbana: mais de duas horas por dia")

# A pesquisa Ipsos-Ipec e a tabela de 2022 possuem universos diferentes;
# por isso a reportagem aparece como contexto, e nao como fonte dos graficos.
with st.container(border=True):
    st.markdown("#### Deslocamentos longos, custo e insegurança nas capitais")
    st.caption("Ipsos-Ipec • Pesquisa Viver nas Cidades: Mobilidade Urbana • setembro de 2026")

    indicador_tempo, indicador_coletivo, indicador_seguranca = st.columns(3)
    indicador_tempo.metric("Tempo médio diário", "2h05", "+9 min vs. 2025")
    indicador_coletivo.metric("Uso principal de coletivo", "54%")
    indicador_seguranca.metric("Inseguros ao caminhar", "80%")

    st.write(
        "Em pesquisa on-line com 3.500 pessoas de 16 anos ou mais em dez capitais, "
        "o tempo médio diário de deslocamento subiu de 1h56, em 2025, para 2h05, "
        "em 2026. Quatro em cada dez participantes passam mais de 1h30 por dia em trânsito."
    )
    st.write(
        "O transporte coletivo segue predominante: 54% usam principalmente algum modal "
        "coletivo, enquanto 44% priorizam meios individuais. Porém, seus usuários relatam "
        "um deslocamento médio maior (2h17, contra 1h47 entre quem usa meios individuais)."
    )
    st.write(
        "A reportagem também destaca que lotação, tarifa e demora são problemas importantes. "
        "O custo das passagens limita visitas, lazer, consultas e procura por emprego para "
        "parte dos usuários; além disso, 80% relatam sentir pouca ou nenhuma segurança ao caminhar."
    )
    st.markdown(
        "[Ler a reportagem completa na Ipsos](https://www.ipsos.com/pt-br/"
        "deslocalementos-superiores-a-2-horas-por-dia-marcam-a-rotina-em-10-capitais-brasileiras)"
    )

st.caption(
    "A pesquisa abrange Manaus, Belém, Fortaleza, Recife, Salvador, Belo Horizonte, "
    "Rio de Janeiro, São Paulo, Porto Alegre e Goiânia. Vitória e Brasília não fazem "
    "parte da amostra; os resultados não devem ser comparados diretamente aos percentuais "
    "da Tabela 13 de 2022."
)
