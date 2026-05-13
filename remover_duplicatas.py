import pandas as pd

# Caminho do arquivo de entrada
arquivo_entrada = "nome_do_arquivo.xlsx"

# Caminho do arquivo de saída (sem duplicatas)
arquivo_saida = "planilha_sem_duplicatas.xlsx"

# Ler a planilha
df = pd.read_excel(arquivo_entrada)

# Remover duplicatas com base na coluna "Title"
df_sem_duplicatas = df.drop_duplicates(subset="Title", keep="first")

# Salvar o resultado
df_sem_duplicatas.to_excel(arquivo_saida, index=False)

print("Duplicatas removidas com sucesso!")