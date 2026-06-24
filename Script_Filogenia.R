###Script filogenia###

#Instalar pacotes
install.packages(c(
  "ape",
  "phytools",
  "vegan",
  "readxl",
  "dplyr",
  "writexl"
))
________________________________________
#Carregar pacotes
library(ape)
library(phytools)
library(vegan)
library(readxl)
library(dplyr)
library(writexl)
________________________________________
#Ler a planilha
###A planilha deve conter: Especie	Ameaça1	Ameaça2	... Amazona aestiva	1	0	...

dados <- read_excel(
  "planilhadedados.xlsx"
)

names(dados)[1] <- "Especie"
________________________________________
#Padronizar nomes
#O BirdTree usa "_"
dados$Especie <- trimws(dados$Especie)

dados$Especie <- gsub(
  " ",
  "_",
  dados$Especie
)
________________________________________
#Corrigir nomenclaturas taxonômicas
#Caso necessário:
  dados$Especie <- gsub(
    "Eupsittula_cactorum",
    "Aratinga_cactorum",
    dados$Especie
  )

dados$Especie <- gsub(
  "Guarouba_guarouba",
  "Guaruba_guarouba",
  dados$Especie
)
________________________________________
#Ler BirdTree
trees <- read.tree(
  "AllBirdsEricson1.tre"
)
________________________________________
#Verificar espécies ausentes
setdiff(
  dados$Especie,
  trees[[1]]$tip.label
)
#O resultado ideal:
  character(0)
________________________________________
#Selecionar espécies
especies <- dados$Especie
________________________________________
#Podar apenas uma árvore
#Para o Mantel não precisamos das 1000 árvores.
tree <- drop.tip(
  trees[[1]],
  setdiff(
    trees[[1]]$tip.label,
    especies
  )
)
________________________________________
#Conferir
plot(tree)

length(tree$tip.label)

tree$tip.label
#Deve aparecer 13 espécies.
________________________________________
#Reordenar a planilha
#Precisamos da mesma ordem da árvore.
dados <- dados[
  match(
    tree$tip.label,
    dados$Especie
  ),
]
________________________________________
#Construir matriz de ameaças
ameacas <- dados[, -1]
________________________________________
#Distância filogenética
dist_phylo <- cophenetic(tree)
________________________________________
#Distância entre perfis de ameaças
#Jaccard é o mais indicado para dados binários.
dist_ameacas <- vegdist(
  ameacas,
  method = "jaccard",
  binary = TRUE
)
________________________________________
#Teste de Mantel
mantel_result <- mantel(
  as.dist(dist_phylo),
  dist_ameacas,
  method = "pearson",
  permutations = 9999
)

mantel_result
________________________________________
#Salvar resultado
resultado_final <- data.frame(
  Estatistica_Mantel = mantel_result$statistic,
  P_valor = mantel_result$signif
)

write_xlsx(
  resultado_final,
  "Resultado_Mantel.xlsx"
)
________________________________________
#salvar matriz de ameaças
write_xlsx(
  dados,
  "Matriz_Ameacas_Especies.xlsx"
)
_______________________________________
#salvar a árvore podada utilizada
write.tree(
  tree,
  file = "Arvore_Podada.tre"
)

