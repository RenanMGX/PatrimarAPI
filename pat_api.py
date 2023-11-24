import os
import socket
from fastapi import FastAPI, HTTPException, status, Header, Depends, Request
import json
import pandas
from extraction_imobme import BotExtractionImobme
import credenciais as cd
from tratar_arquivos_excel_imobme import ImobmeExceltoJson
from datetime import datetime

#informa qual é a pasta com os arquivo json
caminho_dados = "dados\\"


def validar_key(key):
    '''
    função que identifica se a key fornecida esta cadastrada no arquivo hashs.json
    '''
    try:
        with open("hashs.json", 'r')as arqui:
            hash_list = json.load(arqui)
        if key in hash_list:
            return hash_list[key]
        else:
            return False
    except:
        return False
    
def registro(key,end_point,status):
    '''
    salva um log informando açoes do usuario da API
    '''
    data = datetime.now().strftime('%d/%m/%Y')
    hora = datetime.now().strftime('%H:%M:%S')
    try:
        with open("log.csv", 'a')as arqui:
            arqui.write(f"{data};{hora};{end_point};{key['nome']};{status}\n")
    except PermissionError:
        print("arquivo 'log.csv' está aberto em outro dispositivo")




def gerar_novos_arquivos(relatorios):
    '''
    executa os script responsaveis por baixar os relatorios .xlsx do imobme e tratar eles transformando em arquivo json
    '''
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
async def contratos_rescindidos(relatorio, colunas=None, x_key: str = Header(default=None), x_novo: bool = Header(default=False), request: Request = None):
    try:
        endereco_ip = request.client.host
        hostname = socket.gethostbyaddr(endereco_ip)
    except:
        hostname = "não encontrado"
    print(hostname)
    # recebe a key fornecida pelo usuario da API e valida se é verdadeira
    hash_valid = validar_key(x_key)
    if hash_valid == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Chave Invalida!")
    
    #se o usuario informar pelo Header x_novo == 'novo" ira executar a função que gera um arquivo novo direto do site do imobme - meteodo muito lento
    if x_novo:
        gerar_novos_arquivos(relatorio)
        registro(key=hash_valid,end_point=relatorio,status="Gerou como um novo")
    
    #as colunas recebidas pelo query parameter serão divididas por ";"
    if colunas != None:
        colunas = colunas.split(";")

    #ira listar os arquivos na pasda Dados se alguns deles tiver o mesmo nome do end-point será armazenado em 'dados'
    dados = []
    for arquivo in os.listdir(caminho_dados):
        if relatorio in arquivo:
            dados.append(f"{caminho_dados}{arquivo}")
    #verifica se algum arquivo foi encontrado na pasta de dados caso sim o valor sera maior que 0 e ira carregar o arquivo que foi informado no end-point
    if len(dados) > 0:
        with open(dados[0], 'r', encoding='utf-8')as arqui:
            dados_retorno = json.load(arqui)
        
        #caso o usuario informou no query parameter as colunas irá executar retornar apenas as colunas informadas para o usuario
        if colunas != None:
            if len(colunas) > 0:
                #irá usar o dataframe do pandas para separar as colunas desejadas e depois transformar como um dicionario com o orients='records
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
                
                #caso as colunas informadas existirem no arquivo ele irá retornar para o usuario
                if bool(df.to_dict()):
                    registro(key=hash_valid,end_point=relatorio,status="OK!")
                    df = df.replace(float('nan'), None)
                    return df.to_dict(orient='records')
                else:
                    registro(key=hash_valid,end_point=relatorio,status="Nenhuma Coluna Encontrada!")
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhuma Coluna Encontrada!")
            else:
                registro(key=hash_valid,end_point=relatorio,status="Campo de Colunas Vazio")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo de Colunas Vazio")
        else:
            registro(key=hash_valid,end_point=relatorio,status="OK!")
            return dados_retorno
    else:
        registro(key=hash_valid,end_point=relatorio,status="Arquivo Não Encontrado")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo não encontrado!")
    
def config():
    '''
    salva em um arquivo json as configurações para iniciar a API como host e a porta
    '''
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