from fastapi import FastAPI, responses
from extraction_imobme import BotExtractionImobme
from tratar_arquivos_excel_imobme import ImobmeExceltoJson
import json
from flask import Flask
import creden

usuario = creden.usuario
senha = creden.senha

bot = BotExtractionImobme(usuario=usuario,senha=senha)
tratar = ImobmeExceltoJson()
arquivos = tratar.tratar_arquivos(['C:\\Projetos\\PatrimarAPI\\downloads\\ContratosRescindidos_22069_20231115-191427.xlsx'])
#arquivos = bot.iniciar_navegador(debug=True)
#arquivos = bot.obter_relatorios(["imobme_contrator_rescindidos"])


app = FastAPI(
    title="PatrimarAPI",
    version="Beta"
)

@app.get('/')
async def test():
    dicti = arquivos
    return dicti



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("pat_api:app", port=80, reload=True)