# ============================================================
# PIPELINE MULTIVARIADO — REVISÃO SISTEMÁTICA
# PSITACÍDEOS AMEAÇADOS NO BRASIL
# ============================================================

# ============================================================
# OBJETIVOS DO SCRIPT
# ============================================================

# Este script realiza análises estatísticas multivariadas
# utilizando dados consolidados por artigo e bioma.

# As análises incluem:

# 1. Kruskal-Wallis
#    - Comparar o número de subtipos de ameaça entre biomas.

# 2. Análise de Correspondência (CA)
#    - Explorar associações entre biomas e subtipos de ameaça.

# 3. Regressão Linear Temporal
#    - Avaliar tendências temporais das publicações científicas.

# 4. Geração automática de gráficos e exportação dos resultados.

# ============================================================
# IMPORTAÇÕES
# ============================================================

import pandas as pd
import numpy as np

from scipy.stats import kruskal
from scipy.stats import linregress

import matplotlib.pyplot as plt
import seaborn as sns

import prince

import os

# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO = r"E:\arquivos\dados_brutos_estatistica.xlsx"

PASTA_SAIDA = r"E:\Resultados_estatisticas_multivariadas"

os.makedirs(PASTA_SAIDA, exist_ok=True)

sns.set(style="whitegrid")

# ============================================================
# LEITURA DA PLANILHA ORIGINAL
# ============================================================

df = pd.read_excel(ARQUIVO)

df.columns = df.columns.str.strip()

# ============================================================
# DEFINIR COLUNA ID
# ============================================================

ID_COL = df.columns[0]

# ============================================================
# ============================================================
# BASE CONSOLIDADA — RIQUEZA DE AMEAÇAS POR ARTIGO
# ============================================================
# ============================================================

riqueza = pd.DataFrame({

    "nº artigo": [
        1,2,3,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,20,
        21,22,22,22,23,24,25,25,27,27,28,29,31,32,33,33,
        33,34,34,35,35,36,38,39,40
    ],

    "Bioma_consolidado": [
        "Caatinga",
        "Mata Atlântica",
        "Mata Atlântica",
        "Pampa",
        "Amazônia",
        "Cerrado",
        "Cerrado",
        "Caatinga",
        "Caatinga",
        "Caatinga",
        "Caatinga",
        "Amazônia",
        "Caatinga",
        "Caatinga",
        "Pantanal",
        "Pantanal",
        "Pantanal",
        "Mata Atlântica",
        "Mata Atlântica",
        "Caatinga",
        "Pantanal",
        "Cerrado",
        "Amazônia",
        "Pantanal",
        "Mata Atlântica",
        "Caatinga",
        "Mata Atlântica",
        "Mata Atlântica",
        "Pampa",
        "Amazônia",
        "Caatinga",
        "Amazônia",
        "Mata Atlântica",
        "Pantanal",
        "Cerrado",
        "Amazônia",
        "Cerrado",
        "Pantanal",
        "Caatinga",
        "Mata Atlântica",
        "Mata Atlântica",
        "Caatinga",
        "Mata Atlântica",
        "Mata Atlântica"
    ],

    "Numero_ameacas": [
        3,2,1,1,3,3,1,1,2,1,1,2,2,1,2,1,1,2,4,
        2,4,4,4,1,3,2,2,1,1,1,1,2,3,2,2,
        2,2,2,1,1,2,2,1,1
    ]

})

# ============================================================
# EXPORTAR BASE CONSOLIDADA
# ============================================================

riqueza.to_excel(

    f"{PASTA_SAIDA}/riqueza_ameacas_por_artigo.xlsx",
    index=False

)

# ============================================================
# ============================================================
# 1. KRUSKAL-WALLIS
# ============================================================
# ============================================================

grupos = []

nomes_biomas = []

for nome, grupo in riqueza.groupby("Bioma_consolidado"):

    grupos.append(grupo["Numero_ameacas"].values)

    nomes_biomas.append(nome)

# ============================================================
# TESTE KRUSKAL
# ============================================================

kw_stat, kw_p = kruskal(*grupos)

# ============================================================
# EXPORTAR RESULTADOS
# ============================================================

resultado_kw = pd.DataFrame({

    "Kruskal_stat": [kw_stat],
    "p_valor": [kw_p]

})

resultado_kw.to_excel(

    f"{PASTA_SAIDA}/kruskal_resultado.xlsx",
    index=False

)

# ============================================================
# BOXPLOT
# ============================================================

plt.figure(figsize=(10, 6))

sns.boxplot(

    data=riqueza,
    x="Bioma_consolidado",
    y="Numero_ameacas"

)

plt.xticks(rotation=45)

plt.title(
    "Número de Subtipos de Ameaça por Bioma"
)

plt.xlabel("Bioma")

plt.ylabel("Número de Subtipos")

plt.tight_layout()

plt.savefig(

    f"{PASTA_SAIDA}/boxplot_ameacas_bioma.png",
    dpi=300

)

plt.close()

# ============================================================
# ============================================================
# 2. ANÁLISE DE CORRESPONDÊNCIA
# ============================================================
# ============================================================

# ============================================================
# REMOVER LINHAS SEM SUBTIPO
# ============================================================

df_ca = df.dropna(subset=["Subtipo"])

# ============================================================
# FUNÇÃO PARA IDENTIFICAR BIOMAS
# ============================================================

BIOMAS_VALIDOS = [

    "Mata Atlântica",
    "Caatinga",
    "Pantanal",
    "Amazônia",
    "Cerrado",
    "Pampa"

]

def identificar_biomas(texto):

    if pd.isna(texto):
        return []

    texto = str(texto)

    encontrados = []

    for b in BIOMAS_VALIDOS:

        if b.lower() in texto.lower():
            encontrados.append(b)

    return encontrados

# ============================================================
# EXPANDIR BIOMAS
# ============================================================

linhas = []

for _, row in df_ca.iterrows():

    biomas = identificar_biomas(row["Bioma"])

    for b in biomas:

        linhas.append({

            "Bioma": b,
            "Subtipo": row["Subtipo"]

        })

df_exp = pd.DataFrame(linhas)

# ============================================================
# MATRIZ CA
# ============================================================

matriz_ca = pd.crosstab(

    df_exp["Bioma"],
    df_exp["Subtipo"]

)

# ============================================================
# EXPORTAR MATRIZ
# ============================================================

matriz_ca.to_excel(

    f"{PASTA_SAIDA}/matriz_correspondencia.xlsx"

)

# ============================================================
# ANÁLISE DE CORRESPONDÊNCIA
# ============================================================

ca = prince.CA(

    n_components=2,
    random_state=42

)

ca = ca.fit(matriz_ca)

# ============================================================
# COORDENADAS
# ============================================================

row_coords = ca.row_coordinates(matriz_ca)

col_coords = ca.column_coordinates(matriz_ca)

# ============================================================
# EXPORTAR COORDENADAS
# ============================================================

row_coords.to_excel(

    f"{PASTA_SAIDA}/coordenadas_biomas_CA.xlsx"

)

col_coords.to_excel(

    f"{PASTA_SAIDA}/coordenadas_subtipos_CA.xlsx"

)

# ============================================================
# BIPLOT
# ============================================================

plt.figure(figsize=(14, 12))

# ============================================================
# BIOMAS
# ============================================================

plt.scatter(

    row_coords[0],
    row_coords[1]

)

for i, txt in enumerate(matriz_ca.index):

    plt.text(

        row_coords.iloc[i, 0],
        row_coords.iloc[i, 1],
        txt,
        fontsize=12,
        fontweight="bold"

    )

# ============================================================
# SUBTIPOS
# ============================================================

plt.scatter(

    col_coords[0],
    col_coords[1]

)

for i, txt in enumerate(matriz_ca.columns):

    plt.text(

        col_coords.iloc[i, 0],
        col_coords.iloc[i, 1],
        txt,
        fontsize=9

    )

plt.axhline(0)

plt.axvline(0)

plt.xlabel("Dimensão 1")

plt.ylabel("Dimensão 2")

plt.title(
    "Análise de Correspondência — Bioma x Subtipo"
)

plt.tight_layout()

plt.savefig(

    f"{PASTA_SAIDA}/correspondencia_bioma_subtipo.png",
    dpi=300

)

plt.close()

# ============================================================
# ============================================================
# 3. REGRESSÃO TEMPORAL
# ============================================================
# ============================================================

# ============================================================
# EXTRAIR ARTIGOS ÚNICOS
# ============================================================

artigos_unicos = (

    df[[ID_COL, "Ano"]]
    .drop_duplicates(subset=[ID_COL])

)

# ============================================================
# CONTAGEM POR ANO
# ============================================================

artigos_ano = (

    artigos_unicos
    .groupby("Ano")
    .size()
    .reset_index(name="Numero_artigos")

)

# ============================================================
# EXPORTAR
# ============================================================

artigos_ano.to_excel(

    f"{PASTA_SAIDA}/artigos_por_ano.xlsx",
    index=False

)

# ============================================================
# REGRESSÃO
# ============================================================

reg = linregress(

    artigos_ano["Ano"],
    artigos_ano["Numero_artigos"]

)

# ============================================================
# RESULTADOS
# ============================================================

resultado_reg = pd.DataFrame({

    "Slope": [reg.slope],
    "Intercept": [reg.intercept],
    "R2": [reg.rvalue ** 2],
    "p_valor": [reg.pvalue]

})

resultado_reg.to_excel(

    f"{PASTA_SAIDA}/regressao_temporal.xlsx",
    index=False

)

# ============================================================
# GRÁFICO TEMPORAL
# ============================================================

plt.figure(figsize=(10, 6))

sns.regplot(

    data=artigos_ano,
    x="Ano",
    y="Numero_artigos"

)

plt.title(
    "Tendência Temporal das Publicações"
)

plt.xlabel("Ano")

plt.ylabel("Número de Artigos")

plt.tight_layout()

plt.savefig(

    f"{PASTA_SAIDA}/tendencia_temporal.png",
    dpi=300

)

plt.close()

# ============================================================
# FINALIZAÇÃO
# ============================================================

print("========================================")
print("PIPELINE MULTIVARIADO FINALIZADO")
print("========================================")

print("")
print("ARQUIVOS GERADOS:")
print("")

print("KRUSKAL:")
print("- kruskal_resultado.xlsx")
print("- riqueza_ameacas_por_artigo.xlsx")
print("- boxplot_ameacas_bioma.png")

print("")
print("CORRESPONDÊNCIA:")
print("- matriz_correspondencia.xlsx")
print("- coordenadas_biomas_CA.xlsx")
print("- coordenadas_subtipos_CA.xlsx")
print("- correspondencia_bioma_subtipo.png")

print("")
print("REGRESSÃO:")
print("- artigos_por_ano.xlsx")
print("- regressao_temporal.xlsx")
print("- tendencia_temporal.png")

print("")
print(f"Resultados salvos em: {PASTA_SAIDA}")

print("========================================")