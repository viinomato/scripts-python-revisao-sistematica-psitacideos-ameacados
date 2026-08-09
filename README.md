# 📊 Scripts de Revisão Sistemática — Psitacídeos Brasileiros

Este repositório reúne os scripts utilizados no processamento, categorização e análise de dados de uma revisão sistemática sobre **psitacídeos brasileiros**, com foco na identificação e análise de ameaças, distribuição por biomas, status de conservação, padrões temporais e relações filogenéticas.

O pipeline está organizado em **9 etapas**, executadas na sequência de 1 a 9.

---

## 🚀 Visão geral do pipeline

```text
1. Remoção de duplicatas
        ↓
2. Filtragem e ranqueamento dos artigos
        ↓
3. Identificação de palavras-chave
        ↓
4. Categorização automática dos artigos
        ↓
5. Estatísticas multivariadas
        ↓
6. Ranking das ameaças e ameaças emergentes
        ↓
7. Análise de Correspondência Múltipla (MCA)
        ↓
8. Modelo Linear Generalizado (GLM)
        ↓
9. Análise filogenética
```

> **Importante:** os scripts utilizam nomes de arquivos e caminhos definidos diretamente no código. Antes da execução, ajuste os caminhos de entrada e saída conforme a estrutura do seu ambiente.

---

# 📁 Scripts

## 1. 🧹 Remoção de duplicatas

**Arquivo:** `1 - remover_duplicatas.py`

Remove registros duplicados da base de artigos utilizando a coluna `Title` como critério e mantém a primeira ocorrência.

**Entrada**
- Planilha Excel definida em `arquivo_entrada`.

**Processamento**
- Leitura da planilha com `pandas`.
- Remoção de duplicatas por título.

**Saída**
- `planilha_sem_duplicatas.xlsx`

O script utiliza `drop_duplicates(subset="Title", keep="first")`. 

---

## 2. 📈 Filtragem e ranqueamento dos artigos

**Arquivo:** `2 - filtragem_rankeamento.py`

Realiza uma filtragem baseada em texto e posteriormente cria um ranking de relevância dos artigos.

### Processamento

1. Normalização do texto:
   - conversão para minúsculas;
   - remoção de acentos.

2. Busca de termos em português e inglês relacionados a:
   - psitacídeos;
   - Brasil;
   - ameaças;
   - população, sobrevivência, reprodução e distribuição.

3. Cálculo de `score_total`.

4. Definição inicial de relevância:
   - artigos com `score_total >= 3` são classificados como selecionados.

5. Classificação textual utilizando:
   - `TF-IDF`;
   - `LogisticRegression`.

6. Cálculo da probabilidade de relevância (`prob_relevant`).

7. Ordenação dos artigos pela probabilidade de relevância.

**Saída principal**
- `artigos_rankeados.xlsx`

---

## 3. 🔎 Identificação de palavras-chave

**Arquivo:** `3 - palavras_chave_encontradas.py`

Analisa os campos `Title` e `Abstract` dos artigos ranqueados para identificar palavras-chave relacionadas ao escopo da revisão.

As palavras-chave abrangem grupos como:

- taxonomia de psitacídeos;
- localização no Brasil;
- ameaças;
- população e ecologia.

Para cada artigo, o script registra:

- `Palavra-chave encontrada`;
- `Local`;
- `Palavras identificadas`.

A localização pode ser:

- `Title`;
- `Abstract`;
- `Title + Abstract`.

**Entrada**
- `artigos_rankeados.xlsx`

**Saída**
- `artigos_palavras_chave_encontradas.xlsx`

---

## 4. 🧠 Categorização automática dos artigos

**Arquivo:** `4 - categorizacao_artigos.py`

Extrai automaticamente variáveis ecológicas e bibliográficas a partir de `Title` e `Abstract`, utilizando listas de termos e regras de busca textual.

### Variáveis extraídas

- Título;
- Resumo;
- Autor;
- Ano;
- Espécie;
- Bioma;
- Estado;
- Tipo de ameaça;
- Subtipo;
- Impacto;
- Intensidade;
- Método.

### Classificação de ameaças

O script separa as ameaças em:

- **Antrópicas**
- **Naturais**

Entre os subtipos contemplados estão, por exemplo:

- perda de habitat;
- fragmentação florestal;
- desmatamento;
- tráfico de fauna;
- caça/perseguição;
- incêndios antrópicos;
- agropecuária;
- mineração;
- pesticidas;
- espécies invasoras;
- eletroplessão/choques elétricos;
- predação natural;
- doenças;
- competição interespecífica;
- eventos climáticos extremos;
- escassez natural de recursos.

Também são identificados impactos, métodos e uma classificação de intensidade em **Qualitativa** ou **Quantitativa**, conforme indicadores encontrados no texto.

**Entrada**
- `Elegibilidade.xlsx`

**Saída**
- `Artigos_Categorizados.xlsx`

---

## 5. 📊 Estatísticas multivariadas

**Arquivo:** `5 - script_estatisticas_multivariadas.py`

Executa análises estatísticas para investigar padrões relacionados às ameaças, aos biomas e à evolução temporal das publicações.

### Análises realizadas

#### Kruskal-Wallis
Compara o número de subtipos de ameaça entre os biomas.

#### Análise de Correspondência (CA)
Explora associações entre:

- biomas;
- subtipos de ameaça.

#### Regressão linear temporal
Avalia a tendência temporal do número de publicações científicas.

O script também consolida a **riqueza de ameaças por artigo e bioma**.

### Principais saídas

- `riqueza_ameacas_por_artigo.xlsx`
- `kruskal_resultado.xlsx`
- `boxplot_ameacas_bioma.png`
- `matriz_correspondencia.xlsx`
- `coordenadas_biomas_CA.xlsx`
- `coordenadas_subtipos_CA.xlsx`
- `correspondencia_bioma_subtipo.png`
- `artigos_por_ano.xlsx`
- `regressao_temporal.xlsx`
- `tendencia_temporal.png`

---

## 6. ⚠️ Ranking das ameaças e ameaças emergentes

**Arquivo:** `6 - RankingAmeacas_AmeacasEmergentes.py`

Realiza análises descritivas e temporais dos subtipos de ameaça identificados na revisão.

### Ranking das ameaças

Calcula:

- frequência absoluta (`N`);
- frequência relativa (`%`);
- posição no ranking.

### Distribuição temporal

Os registros são agrupados por década:

- 1980s;
- 1990s;
- 2000s;
- 2010s;
- 2020s.

### Ameaças emergentes

O script calcula um **índice de emergência** baseado na variação da frequência entre as décadas de 2000 e 2020.

### Visualizações

- ranking das ameaças;
- heatmap de ocorrência por década;
- tendência temporal dos subtipos.

### Saídas

- `ranking_ameacas.png`
- `heatmap_ameacas_decadas.png`
- `tendencia_subtipos.png`
- `ranking_e_ameacas_emergentes.xlsx`

---

## 7. 🧩 Análise de Correspondência Múltipla (MCA)

**Arquivo:** `7 - MCA.py`

Investiga padrões de associação entre três conjuntos de variáveis:

- **Biomas brasileiros**;
- **Categorias de ameaça/status da IUCN**;
- **Subcategorias de ameaças**.

A análise busca identificar proximidade e associação entre essas categorias no espaço multivariado.

### Preparação dos dados

Antes da MCA, o script:

- remove registros de espécies genéricas;
- associa espécies aos grupos IUCN definidos no script;
- expande registros associados a múltiplos biomas;
- padroniza os nomes dos biomas;
- remove categorias de bioma indesejadas;
- remove categorias muito raras;
- mantém as variáveis `Bioma`, `IUCN` e `Subtipo`.

A MCA é executada com duas dimensões principais.

### Saídas

- `MCA_Grafico_Principal.png`
- `MCA_Coordenadas.xlsx`
- `MCA_Contribuicoes.xlsx` — quando disponível.

---

## 8. 📐 Modelo Linear Generalizado (GLM)

**Arquivo:** `8 - GLM.py`

Avalia se a ocorrência de ameaças relacionadas à **exploração humana** varia de acordo com:

- Bioma;
- grupo IUCN;
- interação entre Bioma e IUCN.

### Variável resposta

`exploracao_humana`

- `0` = ausência;
- `1` = presença.

### Modelos avaliados

**Modelo com interação**

```text
exploracao_humana ~ Bioma * IUCN_grupo
```

**Modelo sem interação**

```text
exploracao_humana ~ Bioma + IUCN_grupo
```

Ambos utilizam distribuição **binomial**.

O script testa a interação por meio de uma razão de verossimilhança e seleciona o modelo final de acordo com o resultado do teste.

### Resultados calculados

- resumo do modelo;
- coeficientes;
- Odds Ratios;
- intervalos de confiança;
- valores de p;
- pseudo-R² de McFadden;
- probabilidades preditas;
- tabelas de contingência.

### Saídas

- `Resultados_GLM_ExploracaoHumana.xlsx`
- `Probabilidades_Preditas.xlsx`
- `Probabilidades_Preditas.png`

---

## 9. 🧬 Análise filogenética

**Arquivo:** `9 - Script_Filogenia.R`

Realiza uma análise da relação entre **distância filogenética** e **similaridade dos perfis de ameaças** entre as espécies.

### Etapas

1. Carregamento dos pacotes R:
   - `ape`;
   - `phytools`;
   - `vegan`;
   - `readxl`;
   - `dplyr`;
   - `writexl`.

2. Leitura da matriz de dados contendo:
   - espécie;
   - ameaças binárias.

3. Padronização dos nomes das espécies para o formato utilizado pelo BirdTree.

4. Correção de nomenclaturas taxonômicas quando necessário.

5. Leitura da árvore `AllBirdsEricson1.tre`.

6. Verificação das espécies presentes na árvore.

7. Poda da árvore para manter apenas as espécies analisadas.

8. Reordenação da matriz de ameaças conforme a ordem dos táxons na árvore.

9. Cálculo da distância filogenética utilizando `cophenetic`.

10. Cálculo da distância entre perfis de ameaças utilizando **Jaccard binário**.

11. Aplicação do **teste de Mantel de Pearson**, com `9999` permutações.

### Saídas

- `Resultado_Mantel.xlsx`
- `Matriz_Ameacas_Especies.xlsx`
- `Arvore_Podada.tre`

---

# 🔗 Fluxo de dados

A sequência conceitual dos scripts é:

| Etapa | Script | Função principal |
|---|---|---|
| **1** | `1 - remover_duplicatas.py` | Limpeza e remoção de duplicatas |
| **2** | `2 - filtragem_rankeamento.py` | Filtragem textual e ranking de relevância |
| **3** | `3 - palavras_chave_encontradas.py` | Identificação e localização de palavras-chave |
| **4** | `4 - categorizacao_artigos.py` | Extração e categorização das variáveis |
| **5** | `5 - script_estatisticas_multivariadas.py` | Kruskal-Wallis, CA e regressão temporal |
| **6** | `6 - RankingAmeacas_AmeacasEmergentes.py` | Ranking, distribuição temporal e ameaças emergentes |
| **7** | `7 - MCA.py` | Análise de Correspondência Múltipla |
| **8** | `8 - GLM.py` | Modelo binomial para exploração humana |
| **9** | `9 - Script_Filogenia.R` | Distância filogenética e teste de Mantel |

> A sequência acima representa a organização metodológica do projeto. Alguns scripts possuem arquivos de entrada definidos independentemente no próprio código e, portanto, podem exigir a preparação ou ajuste da base antes da execução.

---

# 🛠️ Tecnologias e bibliotecas

## Python

Os scripts utilizam, conforme a etapa:

- Python 3
- `pandas`
- `numpy`
- `scikit-learn`
- `scipy`
- `statsmodels`
- `matplotlib`
- `seaborn`
- `prince`
- `adjustText`
- `re`
- `unicodedata`
- `os`

## R

A etapa filogenética utiliza:

- `ape`
- `phytools`
- `vegan`
- `readxl`
- `dplyr`
- `writexl`

---

# ⚙️ Instalação

## Python

Instale as principais dependências com:

```bash
pip install pandas numpy scikit-learn scipy statsmodels matplotlib seaborn prince adjustText openpyxl
```

## R

No R/RStudio:

```r
install.packages(c(
  "ape",
  "phytools",
  "vegan",
  "readxl",
  "dplyr",
  "writexl"
))
```

---

# ▶️ Execução

Execute os scripts seguindo a sequência metodológica:

```bash
python "1 - remover_duplicatas.py"
python "2 - filtragem_rankeamento.py"
python "3 - palavras_chave_encontradas.py"
python "4 - categorizacao_artigos.py"
python "5 - script_estatisticas_multivariadas.py"
python "6 - RankingAmeacas_AmeacasEmergentes.py"
python "7 - MCA.py"
python "8 - GLM.py"
```

Em seguida, execute no R:

```r
source("9 - Script_Filogenia.R")
```

---

# 📌 Observações

- Os scripts foram organizados para representar uma sequência de processamento e análise da revisão sistemática.
- Os caminhos dos arquivos de entrada e saída estão definidos diretamente nos scripts e podem precisar de ajustes.
- A etapa 4 utiliza regras baseadas em dicionários e correspondência textual para categorizar os artigos.
- As etapas estatísticas utilizam bases já estruturadas com as variáveis necessárias para cada análise.
- A etapa 9 utiliza uma matriz binária de ameaças por espécie e uma árvore filogenética do BirdTree.
- Os resultados são exportados principalmente em arquivos Excel e figuras em formato PNG.

---

## 👩‍💻 Autora

Projeto desenvolvido por **Vitória Ribeiro**, com foco em revisão sistemática, biodiversidade, conservação e análise de dados de psitacídeos brasileiros.

---

## 📄 Licença

Uso livre para fins acadêmicos e de pesquisa.
