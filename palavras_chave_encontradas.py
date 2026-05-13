import pandas as pd
import re

# Arquivos
arquivo_entrada = "artigos_rankeados.xlsx"
arquivo_saida = "artigos_palavras_chave_encontradas.xlsx"

# Ler planilha
df = pd.read_excel(arquivo_entrada)

# Garantir que não há valores nulos
df["Title"] = df["Title"].fillna("").astype(str)
df["Abstract"] = df["Abstract"].fillna("").astype(str)

# -------------------------
# LISTA DE PALAVRAS-CHAVE (EN + PT)
# -------------------------
palavras_chave = [
    # Grupo taxonômico
    r"\bpsittacidae\b", r"\bparrot(s)?\b", r"\bmacaw(s)?\b", r"\bparakeet(s)?\b",
    r"psitac[ií]deo(s)?", r"arara(s)?", r"papagaio(s)?", r"periquito(s)?",

    # Local
    r"\bbrazil(ian)?\b", r"brasil",

    # Ameaças
    r"\bthreat(s)?\b", r"habitat loss", r"trafficking", r"hunting", r"wildfire(s)?", r"disease(s)?", r"climate change",
    r"ameaça(s)?", r"desmatamento", r"tr[áa]fico", r"caça", r"inc[êe]ndio(s)?", r"doen[çc]a(s)?", r"mudan[çc]as clim[áa]ticas",

    # População/ecologia
    r"\bpopulation(s)?\b", r"survival", r"reproduction", r"distribution",
    r"popula[çc][ãa]o", r"sobreviv[êe]ncia", r"reprodu[çc][ãa]o", r"distribui[çc][ãa]o"
]

# -------------------------
# FUNÇÃO DE DETECÇÃO
# -------------------------
def analisar_linha(title, abstract):
    title_lower = title.lower()
    abstract_lower = abstract.lower()

    palavras_encontradas = set()
    local_encontro = set()

    for padrao in palavras_chave:
        if re.search(padrao, title_lower):
            palavras_encontradas.add(padrao)
            local_encontro.add("Title")

        if re.search(padrao, abstract_lower):
            palavras_encontradas.add(padrao)
            local_encontro.add("Abstract")

    encontrou = len(palavras_encontradas) > 0

    # Definir localização
    if local_encontro == {"Title"}:
        local = "Title"
    elif local_encontro == {"Abstract"}:
        local = "Abstract"
    elif local_encontro == {"Title", "Abstract"}:
        local = "Title + Abstract"
    else:
        local = ""

    return pd.Series([
        encontrou,
        local,
        ", ".join(sorted(palavras_encontradas))
    ])

# Aplicar análise
df[["Palavra-chave encontrada", "Local", "Palavras identificadas"]] = df.apply(
    lambda row: analisar_linha(row["Title"], row["Abstract"]),
    axis=1
)

# Salvar resultado
df.to_excel(arquivo_saida, index=False)

print("Classificação concluída!")