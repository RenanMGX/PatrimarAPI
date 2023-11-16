import json

arquivo = ""
with open('test123.json', 'r', encoding='utf-8')as arqui:
    arquivo = json.load(arqui)

print(arquivo)