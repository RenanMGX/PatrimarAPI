import os
from fastapi import FastAPI, HTTPException, status, Header, Depends
import json
import pandas
from extraction_imobme import BotExtractionImobme
import credenciais as cd
from tratar_arquivos_excel_imobme import ImobmeExceltoJson

caminho_dados = "dados\\"


def validar_key(key):
    valid_key = ["sdf49as8ef1489da14fa9s8g4"]
    if key in valid_key:
        return True
    return False

def gerar_novos_arquivos(relatorios):
    imobme = BotExtractionImobme(usuario=cd.usuario,senha=cd.senha)
    print(relatorios)
    relat = imobme.obter_relatorios([relatorios])
    tratar = ImobmeExceltoJson()  
    tratar.tratar_arquivos(relat)


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
         
         )
async def contratos_rescindidos(relatorio, colunas=None, x_key: str = Header(default=None), x_novo: bool = Header(default=False)):
    #if not validar_key(x_key):
    #    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Chave Invalida!")
    
    if x_novo:
        gerar_novos_arquivos(relatorio)
    
    
    if colunas != None:
        colunas = colunas.split(";")

    dados = []
    for arquivo in os.listdir(caminho_dados):
        if relatorio in arquivo:
            dados.append(f"{caminho_dados}{arquivo}")
    if len(dados) > 0:
        with open(dados[0], 'r', encoding='utf-8')as arqui:
            dados_retorno = json.load(arqui)
        
        if colunas != None:
            if len(colunas) > 0:
                dataframe_colunas = []
                df = pandas.DataFrame(dados_retorno)
                for coluna in colunas:
                    try:
                        dataframe_colunas.append(df[[coluna]])
                    except:
                        continue
                df = pandas.DataFrame()
                for dataframe in dataframe_colunas:
                    df = pandas.concat([df, dataframe], axis=1)
                
                if bool(df.to_dict()):
                    return df.to_dict(orient='records')
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhuma Coluna Encontrada!")
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo de Colunas Vazio")
        else:
            return dados_retorno
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo não encontrado!")
    
def config():
    default_config = {
        "host" : "0.0.0.0",
        "port" : 8000,
        #"reload" : False
    }
    try:
        with open("config_api.json", 'r')as arqui:
            return json.load(arqui)
    except:
        with open("config_api.json", 'w')as arqui:
            json.dump(default_config, arqui)
            return default_config


if __name__ == "__main__":
    import uvicorn
    
    termos = config()
    #uvicorn.run(app=app, host=termos['host'] , port=termos['port'], reload=True)
    uvicorn.run("pat_api:app", host=termos['host'] , port=termos['port'], reload=True)