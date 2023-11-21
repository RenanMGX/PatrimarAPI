import pandas as pd
meu_dict = {'a': [1], 'b': [2], 'c': [3], 'd': [4], 'e': [5]}

# Especifica as três chaves desejadas
chaves_desejadas = ['a', 'b','e']

# Obtém os valores correspondentes às chaves desejadas
#valores_desejados = [meu_dict[chave] for chave in chaves_desejadas]
df = pd.DataFrame(meu_dict)
df1 = df[['a']]
df2 = df[['e']]
df3 = df[['d']]

df = pd.concat([df1,df2], axis=1)
df = pd.concat([df,df3], axis=1)

print(df)



