# ============================================================
# PIPELINE ESTATÍSTICO — REVISÃO SISTEMÁTICA
# PSITACÍDEOS AMEAÇADOS NO BRASIL
# ============================================================
# ============================================================
# OBJETIVOS
# ============================================================

# 1. Frequências absolutas e relativas
# 2. Teste de McNemar
# 3. Qui-quadrado:
#       - ameaça x bioma
#       - ameaça x espécie
#       - ameaça x status IUCN
# 4. Cramér's V
# 5. Resíduos padronizados
# 6. Gráficos automáticos
# 7. Exportação automática dos resultados
# ============================================================
# IMPORTAÇÕES
# ============================================================

import pandas as pd
import numpy as np

from scipy.stats import chi2_contingency
from statsmodels.stats.contingency_tables import mcnemar

import matplotlib.pyplot as plt
import seaborn as sns

import os

# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_SAIDA = r"E:\Pastadesaida"

os.makedirs(PASTA_SAIDA, exist_ok=True)

TOTAL_ARTIGOS = 40

sns.set(style="whitegrid")

# ============================================================
# FREQUÊNCIA — TIPOS DE AMEAÇA
# ============================================================

freq_ameaca = pd.DataFrame({

    "Tipo de ameaça": [
        "Antrópica",
        "Natural"
    ],

    "Frequência": [
        38,
        11
    ]

})

freq_ameaca["Frequência relativa (%)"] = (
    freq_ameaca["Frequência"] / TOTAL_ARTIGOS * 100
)

freq_ameaca.to_excel(
    f"{PASTA_SAIDA}/frequencia_tipo_ameaca.xlsx",
    index=False
)

# ============================================================
# TESTE DE MCNEMAR
# ============================================================

#                 Natural Sim   Natural Não
# Antrópica Sim        9             29
# Antrópica Não        2              0

tabela_mcnemar = np.array([
    [9, 29],
    [2, 0]
])

resultado_mcnemar = mcnemar(
    tabela_mcnemar,
    exact=True
)

mcnemar_df = pd.DataFrame({

    "Estatística": [resultado_mcnemar.statistic],
    "p-valor": [resultado_mcnemar.pvalue]

})

mcnemar_df.to_excel(
    f"{PASTA_SAIDA}/teste_mcnemar.xlsx",
    index=False
)

# ============================================================
# TABELA — ESPÉCIES
# ============================================================

cont_especie = pd.DataFrame({

    "Antrópica": [7, 6, 3, 3, 3],
    "Natural": [5, 2, 2, 1, 1]

},

index=[

    "Anodorhynchus hyacinthinus",
    "Amazona aestiva",
    "Amazona vinacea",
    "Ara ararauna",
    "Primolius maracana"

])

# ============================================================
# FREQUÊNCIAS RELATIVAS — ESPÉCIES
# ============================================================

freq_rel_especies = pd.DataFrame({

    "Espécie": [

        "Anodorhynchus hyacinthinus",
        "Amazona aestiva",
        "Amazona vinacea",
        "Ara ararauna",
        "Primolius maracana"

    ],

    "Ameaça antrópica associada (%)": [
        17.5,
        15.0,
        7.5,
        7.5,
        7.5
    ],

    "Ameaça natural associada (%)": [
        12.5,
        5.0,
        5.0,
        2.5,
        2.5
    ]

})

cont_especie.to_excel(
    f"{PASTA_SAIDA}/frequencia_especies.xlsx"
)

freq_rel_especies.to_excel(
    f"{PASTA_SAIDA}/frequencia_relativa_especies.xlsx",
    index=False
)

# ============================================================
# QUI-QUADRADO — ESPÉCIES
# ============================================================

chi2_esp, p_esp, gl_esp, expected_esp = (
    chi2_contingency(cont_especie)
)

n_esp = cont_especie.sum().sum()

k_esp = min(cont_especie.shape)

cramer_esp = np.sqrt(
    chi2_esp / (n_esp * (k_esp - 1))
)

residuos_esp = (
    cont_especie - expected_esp
) / np.sqrt(expected_esp)

resultado_especie = pd.DataFrame({

    "Qui-quadrado": [chi2_esp],
    "p-valor": [p_esp],
    "GL": [gl_esp],
    "Cramers_V": [cramer_esp]

})

resultado_especie.to_excel(
    f"{PASTA_SAIDA}/quiquadrado_especies.xlsx",
    index=False
)

residuos_esp.to_excel(
    f"{PASTA_SAIDA}/residuos_especies.xlsx"
)

# ============================================================
# TABELA — BIOMAS
# ============================================================

cont_bioma = pd.DataFrame({

    "Antrópica": [11, 12, 6, 6, 5, 3, 3, 1],
    "Natural": [5, 0, 3, 0, 0, 2, 2, 1]

},

index=[

    "Mata Atlântica",
    "Caatinga",
    "Pantanal",
    "Amazônia",
    "Cerrado",
    "Múltiplos biomas",
    "Não especificado",
    "Pampa"

])

# ============================================================
# FREQUÊNCIAS RELATIVAS — BIOMAS
# ============================================================

freq_rel_bioma = pd.DataFrame({

    "Bioma": [

        "Mata Atlântica",
        "Caatinga",
        "Pantanal",
        "Amazônia",
        "Cerrado",
        "Múltiplos biomas",
        "Não especificado",
        "Pampa"

    ],

    "Ameaça antrópica associada (%)": [
        27.5,
        30.0,
        15.0,
        15.0,
        12.5,
        7.5,
        7.5,
        2.5
    ],

    "Ameaça natural associada (%)": [
        12.5,
        0.0,
        7.5,
        0.0,
        0.0,
        5.0,
        5.0,
        2.5
    ]

})

cont_bioma.to_excel(
    f"{PASTA_SAIDA}/frequencia_biomas.xlsx"
)

freq_rel_bioma.to_excel(
    f"{PASTA_SAIDA}/frequencia_relativa_biomas.xlsx",
    index=False
)

# ============================================================
# QUI-QUADRADO — BIOMAS
# ============================================================

chi2_bio, p_bio, gl_bio, expected_bio = (
    chi2_contingency(cont_bioma)
)

n_bio = cont_bioma.sum().sum()

k_bio = min(cont_bioma.shape)

cramer_bio = np.sqrt(
    chi2_bio / (n_bio * (k_bio - 1))
)

residuos_bio = (
    cont_bioma - expected_bio
) / np.sqrt(expected_bio)

resultado_bioma = pd.DataFrame({

    "Qui-quadrado": [chi2_bio],
    "p-valor": [p_bio],
    "GL": [gl_bio],
    "Cramers_V": [cramer_bio]

})

resultado_bioma.to_excel(
    f"{PASTA_SAIDA}/quiquadrado_biomas.xlsx",
    index=False
)

residuos_bio.to_excel(
    f"{PASTA_SAIDA}/residuos_biomas.xlsx"
)

# ============================================================
# STATUS IUCN E MMA
# ============================================================

status_df = pd.DataFrame({

    "Espécie": [

        "Anodorhynchus hyacinthinus",
        "Amazona aestiva",
        "Amazona vinacea",
        "Ara ararauna",
        "Primolius maracana"

    ],

    "IUCN": [
        "VU",
        "NT",
        "EN",
        "LC",
        "NT"
    ],

    "MMA": [
        "VU",
        "NT",
        "VU",
        "LC",
        "LC"
    ]

})

# ============================================================
# ADICIONAR STATUS
# ============================================================

cont_especie_reset = cont_especie.reset_index()

cont_especie_reset.columns = [
    "Espécie",
    "Antrópica",
    "Natural"
]

df_status = cont_especie_reset.merge(
    status_df,
    on="Espécie",
    how="left"
)

# ============================================================
# IUCN
# ============================================================

cont_iucn = df_status.groupby("IUCN")[
    ["Antrópica", "Natural"]
].sum()

chi2_iucn, p_iucn, gl_iucn, expected_iucn = (
    chi2_contingency(cont_iucn)
)

n_iucn = cont_iucn.sum().sum()

k_iucn = min(cont_iucn.shape)

cramer_iucn = np.sqrt(
    chi2_iucn / (n_iucn * (k_iucn - 1))
)

residuos_iucn = (
    cont_iucn - expected_iucn
) / np.sqrt(expected_iucn)

resultado_iucn = pd.DataFrame({

    "Qui-quadrado": [chi2_iucn],
    "p-valor": [p_iucn],
    "GL": [gl_iucn],
    "Cramers_V": [cramer_iucn]

})

resultado_iucn.to_excel(
    f"{PASTA_SAIDA}/quiquadrado_iucn.xlsx",
    index=False
)

residuos_iucn.to_excel(
    f"{PASTA_SAIDA}/residuos_iucn.xlsx"
)

# ============================================================
# MMA
# ============================================================

cont_mma = df_status.groupby("MMA")[
    ["Antrópica", "Natural"]
].sum()

# ============================================================
# GRÁFICO — TIPOS DE AMEAÇA
# ============================================================

plt.figure(figsize=(7, 5))

sns.barplot(
    data=freq_ameaca,
    x="Tipo de ameaça",
    y="Frequência"
)

plt.title("Frequência dos Tipos de Ameaça")

plt.tight_layout()

plt.savefig(
    f"{PASTA_SAIDA}/grafico_tipos_ameaca.png",
    dpi=300
)

plt.close()

# ============================================================
# HEATMAP — ESPÉCIES
# ============================================================

plt.figure(figsize=(9, 5))

ax = sns.heatmap(
    cont_especie,
    annot=True,
    fmt="d",
    cmap="Blues"
)

# ITÁLICO NAS ESPÉCIES

ax.set_yticklabels(
    ax.get_yticklabels(),
    fontstyle="italic"
)

plt.title("Espécies x Tipo de Ameaça")

plt.tight_layout()

plt.savefig(
    f"{PASTA_SAIDA}/heatmap_especies.png",
    dpi=300
)

plt.close()

# ============================================================
# HEATMAP — BIOMAS
# ============================================================

cont_bioma_plot = cont_bioma.drop(

    index=[
        "Múltiplos biomas",
        "Não especificado"
    ],

    errors="ignore"
)

plt.figure(figsize=(8, 6))

sns.heatmap(
    cont_bioma_plot,
    annot=True,
    fmt="d",
    cmap="YlOrRd"
)

plt.title("Biomas x Tipo de Ameaça")

plt.tight_layout()

plt.savefig(
    f"{PASTA_SAIDA}/heatmap_biomas.png",
    dpi=300
)

plt.close()

# ============================================================
# HEATMAP — STATUS DE CONSERVAÇÃO
# ============================================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 5)
)

# ============================================================
# IUCN
# ============================================================

sns.heatmap(
    cont_iucn,
    annot=True,
    fmt="d",
    cmap="Greens",
    ax=axes[0]
)

axes[0].set_title("IUCN x Tipo de Ameaça")

# ============================================================
# MMA
# ============================================================

sns.heatmap(
    cont_mma,
    annot=True,
    fmt="d",
    cmap="Oranges",
    ax=axes[1]
)

axes[1].set_title("MMA x Tipo de Ameaça")

# ============================================================
# SALVAR
# ============================================================

plt.tight_layout()

plt.savefig(
    f"{PASTA_SAIDA}/heatmap_status_conservacao.png",
    dpi=300
)

plt.close()

# ============================================================
# FINALIZAÇÃO
# ============================================================

print("========================================")
print("PIPELINE ESTATÍSTICO FINALIZADO")
print("========================================")
print(f"Resultados salvos em: {PASTA_SAIDA}")
print("========================================")
print("ARQUIVOS GERADOS:")
print("")
print("FREQUÊNCIAS:")
print("- frequencia_tipo_ameaca.xlsx")
print("- frequencia_especies.xlsx")
print("- frequencia_biomas.xlsx")
print("")
print("TESTES:")
print("- teste_mcnemar.xlsx")
print("- quiquadrado_especies.xlsx")
print("- quiquadrado_biomas.xlsx")
print("- quiquadrado_iucn.xlsx")
print("")
print("RESÍDUOS:")
print("- residuos_especies.xlsx")
print("- residuos_biomas.xlsx")
print("- residuos_iucn.xlsx")
print("")
print("GRÁFICOS:")
print("- grafico_tipos_ameaca.png")
print("- heatmap_especies.png")
print("- heatmap_biomas.png")
print("- heatmap_status_conservacao.png")
print("========================================")