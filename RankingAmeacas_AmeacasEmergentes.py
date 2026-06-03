# ==========================================================
## RANKING DAS AMEAÇAS MAIS COMUNS E AMEAÇAS EMERGENTES
# ==========================================================

# ==========================================================
# OBJETIVOS DO SCRIPT
# ==========================================================

# Este script realiza análises descritivas e temporais dos
# subtipos de ameaça identificados na revisão sistemática.

# As análises incluem:

# 1. Ranking das ameaças mais comuns
#    - Calcula a frequência absoluta (N) de cada subtipo.
#    - Calcula a frequência relativa (%).
#    - Ordena os subtipos do mais frequente para o menos frequente.

# 2. Distribuição temporal das ameaças
#    - Agrupa os registros por década.
#    - Quantifica a frequência de cada subtipo ao longo do tempo.

# 3. Identificação de ameaças emergentes
#    - Calcula um índice de emergência baseado no crescimento
#      da frequência entre as décadas de 2000 e 2020.
#    - Permite identificar ameaças que ganharam relevância
#      recente na literatura científica.

# 4. Geração automática de gráficos
#    - Ranking das ameaças mais comuns.
#    - Heatmap de ocorrência por década.
#    - Tendência temporal dos subtipos.

# 5. Exportação automática dos resultados
#    - Tabela de ranking.
#    - Matriz temporal.
#    - Ranking de ameaças emergentes.
#    - Figuras em alta resolução.

# ==========================================================
# IMPORTAÇÕES
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

ARQUIVO = r"E:\arquivos\dados_brutos_estatistica.xlsx"

PASTA_SAIDA = r"E:\ranking_ameaças_e_ameaças_emergentes"

os.makedirs(PASTA_SAIDA, exist_ok=True)

sns.set(style="whitegrid")

# ==========================================================
# LEITURA DA PLANILHA
# ==========================================================

df = pd.read_excel(ARQUIVO)

# ==========================================================
# LIMPEZA DOS DADOS
# ==========================================================

df["Subtipo"] = (
    df["Subtipo"]
    .astype(str)
    .str.strip()
)

df["Ano"] = pd.to_numeric(
    df["Ano"],
    errors="coerce"
)

df = df.dropna(
    subset=["Ano", "Subtipo"]
)

# ==========================================================
# 1. RANKING DAS AMEAÇAS MAIS COMUNS
# ==========================================================

ranking = (
    df["Subtipo"]
    .value_counts()
    .reset_index()
)

ranking.columns = [
    "Subtipo",
    "N"
]

ranking["Percentual"] = (

    ranking["N"]
    /
    ranking["N"].sum()
    * 100

).round(2)

ranking["Ranking"] = range(
    1,
    len(ranking) + 1
)

ranking = ranking[
    [
        "Ranking",
        "Subtipo",
        "N",
        "Percentual"
    ]
]

# ==========================================================
# GRÁFICO DO RANKING
# ==========================================================

plt.figure(figsize=(10, 6))

sns.barplot(
    data=ranking,
    y="Subtipo",
    x="N"
)

plt.title(
    "Ranking das ameaças mais comuns"
)

plt.xlabel(
    "Frequência absoluta"
)

plt.ylabel(
    "Subtipo"
)

plt.tight_layout()

plt.savefig(
    f"{PASTA_SAIDA}/ranking_ameacas.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==========================================================
# 2. CRIAÇÃO DAS DÉCADAS
# ==========================================================

def definir_decada(ano):

    if ano < 1990:
        return "1980s"

    elif ano < 2000:
        return "1990s"

    elif ano < 2010:
        return "2000s"

    elif ano < 2020:
        return "2010s"

    else:
        return "2020s"

df["Decada"] = df["Ano"].apply(
    definir_decada
)

# ==========================================================
# MATRIZ TEMPORAL
# ==========================================================

matriz_temporal = pd.crosstab(
    df["Subtipo"],
    df["Decada"]
)

# ==========================================================
# GARANTIR TODAS AS DÉCADAS
# ==========================================================

for col in [
    "1980s",
    "1990s",
    "2000s",
    "2010s",
    "2020s"
]:

    if col not in matriz_temporal.columns:
        matriz_temporal[col] = 0

matriz_temporal = matriz_temporal[
    [
        "1980s",
        "1990s",
        "2000s",
        "2010s",
        "2020s"
    ]
]

# ==========================================================
# 3. IDENTIFICAÇÃO DAS AMEAÇAS EMERGENTES
# ==========================================================

emergentes = matriz_temporal.copy()

emergentes["Indice_emergencia"] = (

    (
        emergentes["2020s"]
        -
        emergentes["2000s"]
    )

    /

    (
        emergentes["2000s"] + 1
    )

).round(3)

emergentes = (

    emergentes
    .sort_values(
        "Indice_emergencia",
        ascending=False
    )

)

# ==========================================================
# HEATMAP
# ==========================================================

plt.figure(figsize=(10, 6))

sns.heatmap(
    matriz_temporal,
    annot=True,
    cmap="YlOrRd"
)

plt.title(
    "Ocorrência dos subtipos de ameaça por década"
)

plt.tight_layout()

plt.savefig(
    f"{PASTA_SAIDA}/heatmap_ameacas_decadas.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==========================================================
# GRÁFICO TEMPORAL DOS SUBTIPOS
# ==========================================================

plt.figure(figsize=(12, 7))

for subtipo in matriz_temporal.index:

    plt.plot(
        matriz_temporal.columns,
        matriz_temporal.loc[subtipo],
        marker="o",
        label=subtipo
    )

plt.title(
    "Tendência temporal dos subtipos de ameaça"
)

plt.xlabel(
    "Década"
)

plt.ylabel(
    "Número de registros"
)

plt.legend(
    bbox_to_anchor=(1.05, 1),
    loc="upper left"
)

plt.tight_layout()

plt.savefig(
    f"{PASTA_SAIDA}/tendencia_subtipos.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==========================================================
# EXPORTAÇÃO DOS RESULTADOS
# ==========================================================

with pd.ExcelWriter(
    f"{PASTA_SAIDA}/ranking_e_ameacas_emergentes.xlsx"
) as writer:

    ranking.to_excel(
        writer,
        sheet_name="Ranking_ameacas",
        index=False
    )

    matriz_temporal.to_excel(
        writer,
        sheet_name="Matriz_temporal"
    )

    emergentes.to_excel(
        writer,
        sheet_name="Ameacas_emergentes"
    )

# ==========================================================
# FINALIZAÇÃO
# ==========================================================

print()
print("====================================")
print("ANÁLISE CONCLUÍDA")
print("====================================")
print()

print("Arquivos gerados:")
print()

print(f"{PASTA_SAIDA}/ranking_ameacas.png")
print(f"{PASTA_SAIDA}/heatmap_ameacas_decadas.png")
print(f"{PASTA_SAIDA}/tendencia_subtipos.png")
print(f"{PASTA_SAIDA}/ranking_e_ameacas_emergentes.xlsx")

print()
print(f"Resultados salvos em: {PASTA_SAIDA}")
print("====================================")