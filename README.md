# scripts-python-revisao-sistematica-psitacideos-ameacados

# 📊 Scripts de Revisão Sistemática - Psitacídeos Brasileiros

Este repositório contém um conjunto de scripts em Python desenvolvidos para apoiar uma **revisão sistemática sobre psitacídeos brasileiros**, automatizando etapas como limpeza de dados, filtragem, categorização e análise de artigos científicos.

---

## 🚀 Visão Geral do Pipeline

Os scripts seguem uma sequência lógica:

1. Remoção de duplicatas
2. Filtragem e ranqueamento de artigos
3. Identificação de palavras-chave
4. Categorização automática de variáveis

---

## 📁 Scripts Disponíveis

### 1. 🧹 Remoção de Duplicatas

Arquivo: `remover_duplicatas.py`

Remove registros duplicados com base no título dos artigos.

* Entrada: arquivo Excel
* Saída: nova planilha sem duplicatas

📌 Baseado na coluna `Title`

---

### 2. 📈 Filtragem e Ranqueamento

Arquivo: `filtragem_rankeamento.py`

Aplica um processo híbrido de:

* Regras por palavras-chave (regex)
* Classificação com Machine Learning (TF-IDF + Logistic Regression)

Gera:

* Score de relevância
* Probabilidade de relevância
* Ranking dos artigos

---

### 3. 🔎 Identificação de Palavras-chave

Arquivo: `palavras_chave_encontradas.py`

Analisa Title e Abstract para identificar:

* Presença de palavras-chave
* Local onde foram encontradas
* Lista das palavras identificadas


---

### 4. 🧠 Categorização Automática

Arquivo: `categorizacao_artigos.py`

Extrai automaticamente diversas variáveis dos artigos:

* Espécie
* Bioma
* Estado
* Tipo de ameaça (antrópica/natural)
* Subtipo de ameaça
* Impacto
* Método
* Intensidade (qualitativa/quantitativa)

Utiliza dicionários e regras heurísticas baseadas em texto.


---

## 🧪 Tecnologias Utilizadas

* Python 3.14.4
* pandas
* scikit-learn
* regex (re)
* unicodedata

---

## 📂 Estrutura Esperada dos Dados

Os scripts utilizam arquivos Excel contendo, no mínimo:

* `Title`
* `Abstract`

Colunas opcionais:

* `Authors`
* `Year`

---

## ⚙️ Como Usar

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
```

2. Instale as dependências:

```bash
pip install pandas scikit-learn openpyxl
```

3. Ajuste os caminhos dos arquivos dentro dos scripts

4. Execute os scripts na ordem desejada:

```bash
python remover_duplicatas.py
python filtragem_rankeamento.py
python palavras_chave_encontradas.py
python categorizacao_artigos.py
```

---

## 📌 Observações

* Os scripts são modulares e podem ser usados separadamente
* Os critérios de filtragem e categorização podem ser facilmente ajustados
* O modelo de classificação é treinado automaticamente com base nos dados fornecidos

---

## 👨‍💻 Autor

Projeto desenvolvido para apoio em análise de dados e revisão sistemática com foco em biodiversidade e conservação, por Vitória Ribeiro.

---

## 📄 Licença

Uso livre para fins acadêmicos e de pesquisa.
