import pandas as pd
import requests
from bs4 import BeautifulSoup

with open("12KST.html", 'r', encoding="utf-8")as arqui:
    pagina = arqui.read()


#print(pagina.replace("&nbsp;", ""))
pagina = pagina.replace("&nbsp;", "")


#with open('html_tratado.html', 'w', encoding="utf-8")as arqui:
#    arqui.write(str(pagina))


soup = BeautifulSoup(pagina)

tabela = soup.find_all("tr")

for tr in tabela:
    linhas = tr.find_all("td")
    for td in linhas:
        print(f"{td} - test")
    
    print("fim")
    break

print(len(tabela))
