# 📊 Scripts de Revisão Sistemática - Psitacídeos Brasileiros

Este repositório contém um conjunto de scripts em Python desenvolvidos para apoiar uma **revisão sistemática sobre psitacídeos brasileiros**, automatizando etapas como limpeza de dados, filtragem, categorização e análise de artigos científicos.

***

## 🚀 Visão Geral do Pipeline

Os scripts seguem uma sequência lógica:

1. Remoção de duplicatas
2. Filtragem e ranqueamento de artigos
3. Identificação de palavras-chave
4. Categorização automática de variáveis
5. Estatísticas inferenciais
6. Estatísticas multivariadas
7. Ranking e análise de ameaças

***

## 📁 Scripts Disponíveis

### 1. 🧹 Remoção de Duplicatas

Arquivo: `remover_duplicatas.py`

Remove registros duplicados com base no título dos artigos.

* Entrada: arquivo Excel
* Saída: nova planilha sem duplicatas

📌 Baseado na coluna `Title`

***

### 2. 📈 Filtragem e Ranqueamento

Arquivo: `filtragem_rankeamento.py`

Aplica um processo híbrido de:

* Regras por palavras-chave (regex)
* Classificação com Machine Learning (TF-IDF + Logistic Regression)

Gera:

* Score de relevância
* Probabilidade de relevância
* Ranking dos artigos

***

### 3. 🔎 Identificação de Palavras-chave

Arquivo: `palavras_chave_encontradas.py`

Analisa Title e Abstract para identificar:

* Presença de palavras-chave
* Local onde foram encontradas
* Lista das palavras identificadas

***

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

***

### 5. 📈 Estatísticas Inferenciais

Arquivo: `script_estatisticas_inferenciais.py`

Realiza análises estatísticas para investigar associações entre variáveis ecológicas e tipos de ameaça.

#### 🔍 Inclui:

* Frequências absolutas e relativas
* Teste de McNemar (ameaças antrópicas vs naturais)
* Testes de qui-quadrado:
  * Ameaça × espécie
  * Ameaça × bioma
  * Ameaça × status (IUCN e MMA)
* Cálculo do Cramér's V
* Resíduos padronizados

#### 📊 Saídas:

* Tabelas Excel
* Heatmaps (espécies, biomas, status)
* Gráficos de frequência

***

### 6. 📊 Estatísticas Multivariadas

Arquivo: `script_estatisticas_multivariadas.py`

Executa análises multivariadas para explorar padrões ecológicos.

#### 🔬 Inclui:

* Kruskal-Wallis (comparação entre biomas)
* Análise de Correspondência (CA)
* Regressão linear temporal
* Consolidação de riqueza de ameaças por artigo

#### 📊 Saídas:

* Boxplots
* Biplots (CA)
* Tendência temporal
* Bases consolidadas

***

### 7. ⚠️ Ranking de Ameaças e Ameaças Emergentes

Arquivo: `RankingAmeacas_AmeacasEmergentes.py`

Focado em análise descritiva e temporal das ameaças.

#### 📊 Inclui:

* Ranking das ameaças mais comuns
* Frequência absoluta e relativa
* Distribuição por década
* Identificação de ameaças emergentes (crescimento temporal)

#### 📊 Visualizações:

* Barplot de ranking
* Heatmap por década
* Gráfico de tendência temporal

***

## 🧪 Tecnologias Utilizadas

* Python 3
* pandas
* numpy
* scikit-learn
* scipy
* statsmodels
* seaborn
* matplotlib
* prince (Análise de Correspondência)
* regex (re)
* unicodedata

***

## 📂 Estrutura Esperada dos Dados

Os scripts utilizam arquivos Excel contendo, no mínimo:

* `Title`
* `Abstract`

Para análises estatísticas:

* `Subtipo`
* `Ano`
* `Bioma`
* `Espécie`

Colunas adicionais:

* `Tipo de ameaça`
* `IUCN`
* `MMA`

***

## ⚙️ Como Usar

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
```

2. Instale as dependências:

```bash
pip install pandas numpy scikit-learn scipy statsmodels seaborn matplotlib openpyxl prince
```

3. Ajuste os caminhos dos arquivos dentro dos scripts

4. Execute os scripts na ordem desejada:

```bash
python remover_duplicatas.py
python filtragem_rankeamento.py
python palavras_chave_encontradas.py
python categorizacao_artigos.py
python script_estatisticas_inferenciais.py
python script_estatisticas_multivariadas.py
python RankingAmeacas_AmeacasEmergentes.py
```

***

## 📌 Observações

* Os scripts são modulares e podem ser usados separadamente
* Os critérios podem ser facilmente ajustados
* Todos os scripts exportam automaticamente resultados em Excel e imagens
* O pipeline combina processamento textual com análises estatísticas robustas

***

## 👨‍💻 Autora

Projeto desenvolvido para apoio em análise de dados e revisão sistemática com foco em biodiversidade e conservação, por Vitória Ribeiro.

***

## 📄 Licença

Uso livre para fins acadêmicos e de pesquisa.
