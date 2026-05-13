# ============================================================
# EXTRAÇÃO AUTOMÁTICA DE VARIÁVEIS
# Revisão Sistemática - Psitacídeos brasileiros
# ============================================================

# O script:
# 1. Lê a planilha com os artigos
# 2. Analisa Title + Abstract
# 3. Extrai automaticamente:
#    - Título
#    - Resumo
#    - Autor
#    - Ano
#    - Espécie
#    - Bioma
#    - Estado
#    - Tipo de ameaça
#    - Subtipo
#    - Impacto
#    - Intensidade
#    - Método
# 4. Gera uma nova planilha Excel

# ============================================================

import pandas as pd

# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO_ENTRADA = "Elegibilidade.xlsx"
ARQUIVO_SAIDA = "Artigos_Categorizados.xlsx"

# ============================================================
# LEITURA DA PLANILHA
# ============================================================

df = pd.read_excel(ARQUIVO_ENTRADA)

# ============================================================
# VERIFICAÇÃO DAS COLUNAS
# ============================================================

colunas_necessarias = ["Title", "Abstract"]

for col in colunas_necessarias:
    if col not in df.columns:
        raise Exception(f"Coluna obrigatória não encontrada: {col}")

# ============================================================
# LISTAS DE REFERÊNCIA
# ============================================================

# ---------------- BIOMAS ----------------

biomas = {
    "amazônia": "Amazônia",
    "amazonia": "Amazônia",
    "caatinga": "Caatinga",
    "cerrado": "Cerrado",
    "mata atlântica": "Mata Atlântica",
    "mata atlantica": "Mata Atlântica",
    "pantanal": "Pantanal",
    "pampa": "Pampa"
}

# ---------------- ESTADOS ----------------

estados = {
    "acre": "AC",
    "alagoas": "AL",
    "amapá": "AP",
    "amapa": "AP",
    "amazonas": "AM",
    "bahia": "BA",
    "ceará": "CE",
    "ceara": "CE",
    "distrito federal": "DF",
    "espírito santo": "ES",
    "espirito santo": "ES",
    "goiás": "GO",
    "goias": "GO",
    "maranhão": "MA",
    "maranhao": "MA",
    "mato grosso": "MT",
    "mato grosso do sul": "MS",
    "minas gerais": "MG",
    "pará": "PA",
    "para": "PA",
    "paraíba": "PB",
    "paraiba": "PB",
    "paraná": "PR",
    "parana": "PR",
    "pernambuco": "PE",
    "piauí": "PI",
    "piaui": "PI",
    "rio de janeiro": "RJ",
    "rio grande do norte": "RN",
    "rio grande do sul": "RS",
    "rondônia": "RO",
    "rondonia": "RO",
    "roraima": "RR",
    "santa catarina": "SC",
    "são paulo": "SP",
    "sao paulo": "SP",
    "sergipe": "SE",
    "tocantins": "TO"
}

# ---------------- ESPÉCIES ----------------

especies = [
    "Anodorhynchus leari",
    "Anodorhynchus hyacinthinus",
    "Cyanopsitta spixii",
    "Guaruba guarouba",
    "Amazona aestiva",
    "Amazona vinacea",
    "Ara ararauna",
    "Ara chloropterus",
    "Ara macao",
    "Primolius maracana",
    "Primolius couloni",
    "Pyrrhura griseipectus",
    "Aratinga solstitialis"
]

# ============================================================
# AMEAÇAS ANTRÓPICAS
# ============================================================

ameacas_antropicas = {
    "Perda de habitat": [
        "habitat loss",
        "perda de habitat",
        "degradation",
        "degradação"
    ],

    "Fragmentação florestal": [
        "fragmentation",
        "fragmentação",
        "forest fragment"
    ],

    "Desmatamento": [
        "deforestation",
        "desmatamento",
        "logging"
    ],

    "Tráfico de fauna": [
        "wildlife trade",
        "illegal trade",
        "pet trade",
        "trafficking",
        "tráfico",
        "apreensão",
        "seizure",
        "cetas"
    ],

    "Caça/perseguição": [
        "hunting",
        "poaching",
        "caça",
        "persecution"
    ],

    "Incêndios antrópicos": [
        "wildfire",
        "fire",
        "burning",
        "incêndio",
        "queimada"
    ],

    "Agropecuária": [
        "agriculture",
        "livestock",
        "cattle",
        "farming",
        "agropecuária",
        "pasture"
    ],

    "Mineração": [
        "mining",
        "mineração",
        "mineradora"
    ],

    "Pesticidas": [
        "pesticide",
        "agrochemical",
        "pesticida"
    ],

    "Espécies invasoras": [
        "invasive species",
        "species invasion",
        "espécie invasora"
    ],

    "Eletroplessão/choques elétricos": [
        "electrocution",
        "power line",
        "electric shock",
        "choque elétrico"
    ]
}

# ============================================================
# AMEAÇAS NATURAIS
# ============================================================

ameacas_naturais = {
    "Predação natural": [
        "predation",
        "predação",
        "predator"
    ],

    "Doenças": [
        "disease",
        "pathogen",
        "salmonella",
        "chlamydia",
        "parasite",
        "doença",
        "parasita"
    ],

    "Competição interespecífica": [
        "competition",
        "competição"
    ],

    "Eventos climáticos extremos": [
        "climate change",
        "drought",
        "storm",
        "seca",
        "evento climático"
    ],

    "Escassez natural de recursos": [
        "food shortage",
        "resource limitation",
        "escassez"
    ]
}

# ============================================================
# IMPACTOS
# ============================================================

impactos = {
    "Mortalidade": [
        "mortality",
        "death",
        "mortalidade"
    ],

    "Declínio populacional": [
        "population decline",
        "decline",
        "redução populacional"
    ],

    "Redução reprodutiva": [
        "breeding failure",
        "reproductive decline",
        "baixa reprodução"
    ],

    "Redução de distribuição": [
        "range contraction",
        "distribution reduction"
    ]
}

# ============================================================
# MÉTODOS
# ============================================================

metodos = {
    "Monitoramento": [
        "monitoring",
        "survey",
        "census",
        "monitoramento"
    ],

    "Modelagem": [
        "modeling",
        "ecological niche",
        "sdm",
        "modelagem"
    ],

    "Genética": [
        "genetic",
        "microsatellite",
        "dna"
    ],

    "Telemetria": [
        "telemetry",
        "tracking",
        "gps"
    ],

    "Entrevista/questionário": [
        "interview",
        "questionnaire",
        "ethno",
        "interviewed"
    ]
}

# ============================================================
# FUNÇÕES
# ============================================================

def buscar_termos(texto, dicionario):

    encontrados = []

    for categoria, termos in dicionario.items():

        for termo in termos:

            if termo.lower() in texto:
                encontrados.append(categoria)
                break

    return list(set(encontrados))

# ------------------------------------------------------------

def buscar_especies(texto):

    encontrados = []

    for especie in especies:

        if especie.lower() in texto:
            encontrados.append(especie)

    return list(set(encontrados))

# ------------------------------------------------------------

def buscar_biomas(texto):

    encontrados = []

    for termo, nome in biomas.items():

        if termo in texto:
            encontrados.append(nome)

    return list(set(encontrados))

# ------------------------------------------------------------

def buscar_estados(texto):

    encontrados = []

    for termo, uf in estados.items():

        if termo in texto:
            encontrados.append(uf)

    return list(set(encontrados))

# ============================================================
# EXTRAÇÃO DAS VARIÁVEIS
# ============================================================

resultados = []

for idx, row in df.iterrows():

    # --------------------------------------------------------
    # DADOS BÁSICOS
    # --------------------------------------------------------

    titulo = str(row["Title"]) if pd.notna(row["Title"]) else ""

    resumo = str(row["Abstract"]) if pd.notna(row["Abstract"]) else ""

    texto = f"{titulo} {resumo}".lower()

    # --------------------------------------------------------
    # AUTOR
    # --------------------------------------------------------

    autor = ""

    if "Authors" in df.columns:
        autor = str(row["Authors"])

    # --------------------------------------------------------
    # ANO
    # --------------------------------------------------------

    ano = ""

    if "Year" in df.columns:
        ano = str(row["Year"])

    # --------------------------------------------------------
    # ESPÉCIES
    # --------------------------------------------------------

    especies_encontradas = buscar_especies(texto)

    # --------------------------------------------------------
    # BIOMAS
    # --------------------------------------------------------

    biomas_encontrados = buscar_biomas(texto)

    # --------------------------------------------------------
    # ESTADOS
    # --------------------------------------------------------

    estados_encontrados = buscar_estados(texto)

    # --------------------------------------------------------
    # AMEAÇAS
    # --------------------------------------------------------

    subtipos_antropicos = buscar_termos(
        texto,
        ameacas_antropicas
    )

    subtipos_naturais = buscar_termos(
        texto,
        ameacas_naturais
    )

    tipos_ameaca = []

    if len(subtipos_antropicos) > 0:
        tipos_ameaca.append("Antrópica")

    if len(subtipos_naturais) > 0:
        tipos_ameaca.append("Natural")

    subtipos = subtipos_antropicos + subtipos_naturais

    # --------------------------------------------------------
    # IMPACTOS
    # --------------------------------------------------------

    impactos_encontrados = buscar_termos(
        texto,
        impactos
    )

    # --------------------------------------------------------
    # MÉTODOS
    # --------------------------------------------------------

    metodos_encontrados = buscar_termos(
        texto,
        metodos
    )

    # --------------------------------------------------------
    # INTENSIDADE
    # --------------------------------------------------------

    intensidade = "Qualitativa"

    indicadores_quantitativos = [
        "statistical",
        "regression",
        "density",
        "abundance",
        "occupancy",
        "quantitative",
        "generalized linear model",
        "glm",
        "probability",
        "variance"
    ]

    if any(t in texto for t in indicadores_quantitativos):
        intensidade = "Quantitativa"

    # --------------------------------------------------------
    # RESULTADO FINAL
    # --------------------------------------------------------

    resultados.append({

        "Título": titulo,

        "Resumo": resumo,

        "Autor": autor,

        "Ano": ano,

        "Espécie": "; ".join(especies_encontradas),

        "Bioma": "; ".join(biomas_encontrados),

        "Estado": "; ".join(estados_encontrados),

        "Tipo de ameaça": "; ".join(tipos_ameaca),

        "Subtipo": "; ".join(subtipos),

        "Impacto": "; ".join(impactos_encontrados),

        "Intensidade": intensidade,

        "Método": "; ".join(metodos_encontrados)
    })

# ============================================================
# CRIAR DATAFRAME FINAL
# ============================================================

df_final = pd.DataFrame(resultados)

# ============================================================
# EXPORTAR PARA EXCEL
# ============================================================

df_final.to_excel(ARQUIVO_SAIDA, index=False)

# ============================================================
# FINALIZAÇÃO
# ============================================================

print("\n========================================")
print("PLANILHA GERADA COM SUCESSO")
print("========================================")

print(f"\nArquivo salvo como:")
print(f"{ARQUIVO_SAIDA}")

print(f"\nTotal de artigos processados:")
print(len(df_final))