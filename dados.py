from pathlib import Path
import pandas as pd

RACAS = ['Branca', 'Preta ou Parda', 'Indígena']
MODAIS = ['A pé', 'Bicicleta', 'Motocicleta ou Mototaxi', 'Automóvel, taxi ou assemelhados', 'Transporte coletivo', 'Outros']

def carregar():
    origem = Path(__file__).parent / 'Tabela_13_Meio_de_transporte.xlsx'
    tabela = pd.read_excel(origem, sheet_name='BR GR UF MU', header=None, skiprows=3, engine='calamine')
    blocos = []
    for i, raca in enumerate(RACAS):
        bloco = tabela.iloc[:, [0] + list(range(1 + 6*i, 7 + 6*i))].copy()
        bloco.columns = ['Local'] + MODAIS
        bloco['Cor ou raça'] = raca
        blocos.append(bloco.melt(id_vars=['Local', 'Cor ou raça'], var_name='Transporte', value_name='Percentual'))
    dados = pd.concat(blocos, ignore_index=True)
    dados['Percentual'] = pd.to_numeric(dados['Percentual'], errors='coerce')
    dados['UF'] = dados['Local'].str.extract(r'\(([A-Z]{2})\)$')
    return dados

def agrupar(tabela):
    valores = tabela.set_index('Transporte')['Percentual']
    grupos = {'Coletivo': ['Transporte coletivo'], 'Carro/táxi + moto/mototáxi': MODAIS[2:4], 'Ativo: a pé + bicicleta': MODAIS[:2], 'Outros': ['Outros']}
    return pd.DataFrame([{'Categoria': nome, 'Percentual': valores.reindex(modais).sum(min_count=len(modais))} for nome, modais in grupos.items()])
