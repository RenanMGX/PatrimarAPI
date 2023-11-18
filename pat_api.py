import os
from fastapi import FastAPI, HTTPException, status, Header, Depends
from extraction_imobme import BotExtractionImobme
from tratar_arquivos_excel_imobme import ImobmeExceltoJson
import credenciais
import json
from typing import Dict, List

caminho_dados = "dados\\"
#arquivos = bot.iniciar_navegador(debug=True)
#arquivos = bot.obter_relatorios(["imobme_contratos_rescindidos"])
#arquivos = tratar.tratar_arquivos(['C:\\Projetos\\PatrimarAPI\\downloads\\Empreendimentos_22078_20231116-095153.xlsx','C:\\Projetos\\PatrimarAPI\\downloads\\ContratosRescindidos_22077_20231116-095153.xlsx','C:\\Projetos\\PatrimarAPI\\downloads\\Vendas_22079_20231116-095155.xlsx'])
#print(arquivos)

def validar_key(key):
    valid_key = ["sdf49as8ef1489da14fa9s8g4"]
    if key in valid_key:
        return True
    return False


app = FastAPI(
    title="PatrimarAPI",
    version="Beta"
)

#Relatorios:
#  ContratosRescindidos
#  Empreendimentos
#  Vendas
@app.get('/relatorios_imobme/{relatorio}',
         description="este EndPoint ira retornar um arquivo json do relatorio solicitado os relatorios cadastrados são: 'ContratosRescindidos', 'Empreendimentos', 'Vendas  ",
         response_description=test
         )
async def contratos_rescindidos(relatorio, x_key: str = Header(default=None)):
    #if not validar_key(x_key):
    #    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Chave Invalida!")
    
    dados = []
    for arquivo in os.listdir(caminho_dados):
        if relatorio in arquivo:
            dados.append(f"{caminho_dados}{arquivo}")
    if len(dados) > 0:
        with open(dados[0], 'r', encoding='utf-8')as arqui:
            return json.load(arqui)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo não encontrado!")

if __name__ == "__main__":
    #arquivos = bot.obter_relatorios(["imobme_controle_vendas","imobme_contratos_rescindidos", "imobme_empreendimento"])
    import uvicorn
    
    uvicorn.run("pat_api:app", host="0.0.0.0" , port=7000, reload=True)