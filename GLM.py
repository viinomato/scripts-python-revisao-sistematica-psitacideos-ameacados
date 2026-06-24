# ============================================================
# GLM BINOMIAL
# Exploração humana ~ Bioma + IUCN + interação
#
# Objetivo:
# Avaliar se a ocorrência de ameaças relacionadas à exploração
# humana varia em função:
#   1) do Bioma;
#   2) do status de conservação da IUCN;
#   3) da interação entre essas variáveis.
#
# Variável resposta:
# exploracao_humana
#     0 = ausência
#     1 = presença
#
# Variáveis explicativas:
# Bioma
# IUCN_grupo
#
# Autor: Vitória Ribeiro
# ============================================================

# ============================================================
# 1. Importar bibliotecas
# ============================================================

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ============================================================
# 2. Ler planilha
# ============================================================

df = pd.read_excel(r"E:\Projetos\GLM\dadosbrutos.xlsx")

# ============================================================
# 3. Verificar estrutura dos dados
# ============================================================

print(df.head())
print(df.info())

# ============================================================
# 4. Transformar variáveis em categóricas
# ============================================================

df["Bioma"] = df["Bioma"].astype("category")
df["IUCN_grupo"] = df["IUCN_grupo"].astype("category")

# resposta binária
df["exploracao_humana"] = (
    df["exploracao_humana"]
    .astype(int)
)

# ============================================================
# 5. Tabelas de contingência
# ============================================================

print("\nBioma x Exploração Humana")
print(pd.crosstab(
    df["Bioma"],
    df["exploracao_humana"]
))

print("\nIUCN x Exploração Humana")
print(pd.crosstab(
    df["IUCN_grupo"],
    df["exploracao_humana"]
))

# ============================================================
# 6. Modelo completo
# ============================================================
# Inclui interação entre Bioma e IUCN

modelo_interacao = smf.glm(
    formula=
    "exploracao_humana ~ C(Bioma) * C(IUCN_grupo)",
    data=df,
    family=sm.families.Binomial()
).fit()

# ============================================================
# 7. Modelo sem interação
# ============================================================

modelo_sem_interacao = smf.glm(
    formula=
    "exploracao_humana ~ C(Bioma) + C(IUCN_grupo)",
    data=df,
    family=sm.families.Binomial()
).fit()

# ============================================================
# 8. Resumos
# ============================================================

print("\nMODELO COM INTERAÇÃO")
print(modelo_interacao.summary())

print("\nMODELO SEM INTERAÇÃO")
print(modelo_sem_interacao.summary())

# ============================================================
# 9. Teste da interação
# ============================================================
# Teste da razão de verossimilhança

lr = (
    2 *
    (modelo_interacao.llf -
     modelo_sem_interacao.llf)
)

df_diff = (
    modelo_interacao.df_model -
    modelo_sem_interacao.df_model
)

p = stats.chi2.sf(lr, df_diff)

print("\n===================================")
print("Teste da interação")
print("LR =", lr)
print("GL =", df_diff)
print("p =", p)
print("===================================")

# ============================================================
# 10. Escolher modelo final
# ============================================================

if p < 0.05:
    modelo_final = modelo_interacao
    print("\nInteração significativa.")
    print("Modelo final: Bioma * IUCN")
else:
    modelo_final = modelo_sem_interacao
    print("\nInteração NÃO significativa.")
    print("Modelo final: Bioma + IUCN")

# ============================================================
# 11. Resumo do modelo final
# ============================================================

print(modelo_final.summary())

# ============================================================
# 12. Odds Ratios
# ============================================================

coef = modelo_final.params
conf = modelo_final.conf_int()

or_df = pd.DataFrame({
    "Coeficiente": coef,
    "Odds_Ratio": np.exp(coef),
    "IC_inf": np.exp(conf[0]),
    "IC_sup": np.exp(conf[1]),
    "p_valor": modelo_final.pvalues
})

print("\nOdds Ratios")
print(or_df)

# ============================================================
# 13. Salvar resultados
# ============================================================

or_df.to_excel(
    "Resultados_GLM_ExploracaoHumana.xlsx"
)

# ============================================================
# 14. Pseudo-R² de McFadden
# ============================================================

print("\nPseudo-R² de McFadden")
print(modelo_final.pseudo_rsquared())

# ============================================================
# 15. Probabilidades preditas
# ============================================================

novo = pd.DataFrame([
    (b, i)
    for b in df["Bioma"].cat.categories
    for i in df["IUCN_grupo"].cat.categories
], columns=["Bioma", "IUCN_grupo"])

novo["probabilidade"] = (
    modelo_final.predict(novo)
)

print("\nProbabilidades preditas")
print(novo)

novo.to_excel(
    "Probabilidades_Preditas.xlsx",
    index=False
)

# ============================================================
# 16. Gráfico
# ============================================================

plt.figure(figsize=(8, 6))

sns.barplot(
    data=novo,
    x="Bioma",
    y="probabilidade",
    hue="IUCN_grupo"
)

plt.ylabel(
    "Probabilidade de exploração humana"
)

plt.xlabel("Bioma")

plt.title(
    "Probabilidade predita de ocorrência de exploração humana"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "Probabilidades_Preditas.png",
    dpi=300
)

plt.show()

# ============================================================
# 17. Tabela ANOVA
# ============================================================

from statsmodels.stats.anova import anova_lm

print(
    "\nModelo final ajustado com sucesso."
)
print(modelo_interacao.summary())

print("p interação =", p)

pd.crosstab(
    df["IUCN_grupo"],
    df["exploracao_humana"],
    margins=True
)

pd.crosstab(
    [df["Bioma"], df["IUCN_grupo"]],
    df["exploracao_humana"]
)