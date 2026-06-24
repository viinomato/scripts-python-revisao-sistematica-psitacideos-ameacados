# ==========================================================
# ANÁLISE DE CORRESPONDÊNCIA MÚLTIPLA (MCA)
# ==========================================================
#
# OBJETIVO
#
# Investigar padrões de associação entre:
#
# • Biomas brasileiros
# • Categorias de ameaça da IUCN
# • Subcategorias de ameaças
#
# registradas para psitacídeos brasileiros.
#
# A MCA permitirá identificar:
#
# - quais subcategorias de ameaça se associam
#   a determinados biomas;
#
# - quais categorias da IUCN se aproximam
#   de determinados conjuntos de ameaças;
#
# - o perfil ecológico geral das ameaças
#   reportadas na literatura científica.
#
# ==========================================================

import pandas as pd
import prince
import matplotlib.pyplot as plt
from adjustText import adjust_text
from matplotlib.lines import Line2D
import unicodedata
import re

# ==========================================================
# ARQUIVO
# ==========================================================

ARQUIVO = r"E:\dados_brutos_estatistica.xlsx"

# ==========================================================
# FUNÇÕES
# ==========================================================

def remover_acentos(texto):

    if pd.isna(texto):
        return texto

    texto = str(texto)

    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# ==========================================================
# LEITURA
# ==========================================================

print("\nLendo planilha...")

df = pd.read_excel(ARQUIVO)

print(f"Registros originais: {len(df)}")

# ==========================================================
# REMOVER ESPÉCIES GENÉRICAS
# ==========================================================

especies_excluir = [

    "Múltiplas espécies",
    "Multiplas especies",

    "Múltiplas espécies de psitacídeos",
    "Multiplas especies de psitacideos"

]

df = df[
    ~df["Espécie"].isin(especies_excluir)
]

print(f"Após remover espécies genéricas: {len(df)}")

# ==========================================================
# IUCN
# ==========================================================

iucn_dict = {

    "Anodorhynchus hyacinthinus":"VU",
    "Amazona aestiva":"NT",
    "Amazona vinacea":"EN",
    "Ara ararauna":"LC",
    "Primolius maracana":"NT",
    "Anodorhynchus leari":"EN",
    "Guarouba guarouba":"VU",
    "Alipiopsitta xanthops":"NT",
    "Amazona amazonica":"LC",
    "Amazona brasiliensis":"NT",
    "Amazona ochrocephala":"LC",
    "Amazona pretrei":"VU",
    "Amazona rhodocorytha":"VU",
    "Psittacara leucophthalmus":"LC",
    "Cyanopsitta spixii":"EW",
    "Eupsittula cactorum":"LC",
    "Pionus maximiliani":"LC",
    "Primolius couloni":"VU",
    "Pyrrhura pfrimeri":"EN"

}

df["IUCN"] = df["Espécie"].map(iucn_dict)

# ==========================================================
# EXPANSÃO DOS BIOMAS
# ==========================================================

print("\nExpandindo registros multibioma...")

linhas_expandidas = []

for _, linha in df.iterrows():

    bioma = str(linha["Bioma"])

    bioma = (
        bioma
        .replace(";", "|")
        .replace(",", "|")
        .replace("/", "|")
    )

    lista_biomas = [

        b.strip()

        for b in bioma.split("|")

        if b.strip()
    ]

    if len(lista_biomas) == 0:
        continue

    for b in lista_biomas:

        nova_linha = linha.copy()

        nova_linha["Bioma"] = b

        linhas_expandidas.append(nova_linha)

df = pd.DataFrame(linhas_expandidas)

print(f"Registros após expansão: {len(df)}")

# ==========================================================
# PADRONIZAÇÃO DOS BIOMAS
# ==========================================================

padronizacao = {

    "Amazonia":"Amazônia",
    "Amazônia":"Amazônia",

    "Mata Atlantica":"Mata Atlântica",
    "Mata Atlântica":"Mata Atlântica",

    "Caatinga":"Caatinga",
    "Cerrado":"Cerrado",
    "Pantanal":"Pantanal",
    "Pampa":"Pampa"

}

df["Bioma"] = (
    df["Bioma"]
    .astype(str)
    .str.strip()
)

df["Bioma"] = df["Bioma"].replace(padronizacao)

# ==========================================================
# REMOVER BIOMAS INDESEJADOS
# ==========================================================

termos_excluir = {

    "ecotono",
    "ecotonos",

    "nao especificado",
    "não especificado",

    "multiplos",
    "múltiplos",

    "multiplos biomas",
    "múltiplos biomas"
}

manter = []

for valor in df["Bioma"]:

    v = remover_acentos(
        str(valor).lower()
    ).strip()

    manter.append(v not in termos_excluir)

df = df[manter]

print(f"Após limpeza dos biomas: {len(df)}")

# ==========================================================
# DADOS DA MCA
# ==========================================================

dados_mca = df[
    [
        "Bioma",
        "IUCN",
        "Subtipo"
    ]
].copy()

dados_mca = dados_mca.dropna()

# ==========================================================
# REMOVER CATEGORIAS MUITO RARAS
# ==========================================================

for coluna in dados_mca.columns:

    freq = dados_mca[coluna].value_counts()

    categorias_validas = freq[
        freq >= 2
    ].index

    dados_mca = dados_mca[
        dados_mca[coluna].isin(
            categorias_validas
        )
    ]

print(f"\nRegistros finais: {len(dados_mca)}")

# ==========================================================
# MCA
# ==========================================================

mca = prince.MCA(
    n_components=2,
    n_iter=20,
    copy=True,
    check_input=True,
    engine="sklearn",
    random_state=42
)

mca = mca.fit(dados_mca)

# ==========================================================
# VARIÂNCIA EXPLICADA
# ==========================================================

print("\nVARIÂNCIA EXPLICADA")

eigenvalues = mca.eigenvalues_

for i, eig in enumerate(eigenvalues):

    perc = eig / sum(eigenvalues) * 100

    print(
        f"Dimensão {i+1}: "
        f"{perc:.2f}%"
    )

# ==========================================================
# COORDENADAS
# ==========================================================

coords = mca.column_coordinates(dados_mca)

coords["Categoria"] = coords.index

coords.to_excel(
    r"E:\arquivos\MCA_Coordenadas.xlsx",
    index=False
)

# ==========================================================
# CONTRIBUIÇÕES
# ==========================================================

try:

    contrib = mca.column_contributions_

    contrib.to_excel(
        r"E:\arquivos\MCA_Contribuicoes.xlsx"
    )

except:
    pass

# ==========================================================
# IDENTIFICAÇÃO DOS GRUPOS
# ==========================================================

coords["Grupo"] = coords["Categoria"].apply(
    lambda x:
    "Bioma"
    if str(x).startswith("Bioma__")
    else "IUCN"
    if str(x).startswith("IUCN__")
    else "Subtipo"
)

# ==========================================================
# CORES E SÍMBOLOS
# ==========================================================

cores = {

     "Bioma": "#2E8B57",      # verde
    "IUCN": "#B22222",       # vermelho
    "Subtipo": "#1E90FF"     # azul

}

marcadores = {

    "Bioma": "o",
    "IUCN": "s",
    "Subtipo": "^"

}

# ==========================================================
# GRÁFICO MCA
# ==========================================================

plt.figure(figsize=(16, 12))

plt.axhline(
    0,
    linestyle="--",
    linewidth=0.8,
    color="gray"
)

plt.axvline(
    0,
    linestyle="--",
    linewidth=0.8,
    color="gray"
)

texts = []

coords["Rotulo"] = (
    coords["Categoria"]
    .str.replace("Bioma__", "", regex=False)
    .str.replace("IUCN__", "", regex=False)
    .str.replace("Subtipo__", "", regex=False)
)

coords["Rotulo"] = coords["Rotulo"].replace({
    "Manejo antrópico": "Manejo"
})

for _, row in coords.iterrows():

    x = row[0]
    y = row[1]

    plt.scatter(
        x,
        y,
        color=cores[row["Grupo"]],
        marker=marcadores[row["Grupo"]],
        s=120,
        alpha=0.85
    )

    texts.append(

        plt.text(
            x,
            y,
            row["Rotulo"],
            # row["Categoria"],
            fontsize=9
        )
    )

adjust_text(texts)

# ==========================================================
# LEGENDA
# ==========================================================

legenda = [

    Line2D(
        [0],[0],
        marker='o',
        color='w',
        markerfacecolor=cores["Bioma"],
        markersize=10,
        label='Bioma'
    ),

    Line2D(
        [0],[0],
        marker='s',
        color='w',
        markerfacecolor=cores["IUCN"],
        markersize=10,
        label='IUCN'
    ),

    Line2D(
        [0],[0],
        marker='^',
        color='w',
        markerfacecolor=cores["Subtipo"],
        markersize=10,
        label='Subcategoria'
    )
]

plt.legend(
    handles=legenda,
    frameon=True
)

plt.title(
    "Análise de Correspondência Múltipla (MCA)\nBioma × IUCN × Subcategoria de ameaça",
    fontsize=16
)

plt.xlabel("Dimensão 1")
plt.ylabel("Dimensão 2")

plt.tight_layout()

plt.savefig(
    r"E:\arquivos\MCA_Grafico_Principal.png",
    dpi=600,
    bbox_inches="tight"
)

plt.show()

print("\nArquivos gerados:")
print("- MCA_Grafico_Principal.png")
print("- MCA_Coordenadas.xlsx")
print("- MCA_Contribuicoes.xlsx (quando disponível)")

print("\nAnálise concluída com sucesso.")