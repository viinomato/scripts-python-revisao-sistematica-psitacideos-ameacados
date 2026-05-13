import pandas as pd
import re
import unicodedata

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# =========================
# Normalização de texto
# =========================
def normalize_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text

# =========================
# Regex com plural automático
# =========================
def build_pattern(words):
    patterns = []
    for w in words:
        # plural simples (s opcional)
        w = re.escape(w)
        patterns.append(rf"\b{w}s?\b")
    return re.compile("|".join(patterns))

# =========================
# Palavras-chave (grupos)
# =========================

groups_en = [
    ["psittacidae", "parrot", "macaw", "parakeet"],
    ["brazil", "brazilian"],
    ["threat", "habitat loss", "trafficking", "hunting", "wildfire", "disease", "climate change"],
    ["population", "survival", "reproduction", "distribution"]
]

groups_pt = [
    ["psitacideo", "arara", "papagaio", "periquito"],
    ["brasil"],
    ["ameaca", "desmatamento", "trafico", "caca", "incendio", "doenca", "mudanca climatica"],
    ["populacao", "sobrevivencia", "reproducao", "distribuicao"]
]

# Compilar regex
patterns_en = [build_pattern(g) for g in groups_en]
patterns_pt = [build_pattern(g) for g in groups_pt]

# =========================
# Função de matching + score
# =========================
def match_and_score(text, patterns):
    score = 0
    for p in patterns:
        if p.search(text):
            score += 1
    return score

# =========================
# Carregar dados
# =========================
df = pd.read_excel(r"D:/pasta/Artigo.xlsx")

# =========================
# Criar texto combinado
# =========================
df["text"] = (df["Title"].fillna("") + " " + df["Abstract"].fillna("")).apply(normalize_text)

# =========================
# Aplicar lógica
# =========================
df["score_en"] = df["text"].apply(lambda x: match_and_score(x, patterns_en))
df["score_pt"] = df["text"].apply(lambda x: match_and_score(x, patterns_pt))

# Score total
df["score_total"] = df["score_en"] + df["score_pt"]

# Seleção (mais flexível que antes)
df["selected"] = df["score_total"] >= 3  # você pode ajustar

# =========================
# ===== NLP CLASSIFIER =====
# =========================

# Criar rótulo inicial (fraco, baseado no filtro)
df["label"] = df["selected"].astype(int)

# Vetorização
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df["text"])
y = df["label"]

# Treinar modelo
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Prever probabilidade
df["prob_relevant"] = model.predict_proba(X)[:,1]

# =========================
# Ranking final
# =========================
df = df.sort_values(by="prob_relevant", ascending=False)

# =========================
# Salvar resultados
# =========================
df.to_excel(r"D:/Pasta/Arquivos/artigos_rankeados.xlsx", index=False)

print("Processo finalizado!")
print(df[["Title", "score_total", "prob_relevant"]].head(10))