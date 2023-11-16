import pandas as pd
from tkinter import filedialog as fd
import xlwings as xw
import json
import os
import pygetwindow as gw
from datetime import datetime

class ImobmeExceltoJson():
    def __init__(self):
        self.__dicionatio_final = {}
        self.__exten_excel = ['.xlsx','.xlsm','.xlsb', '.xltx']

    def tratar_arquivos(self,lista_arquivos=['C:\\Projetos\\PatrimarAPI\\downloads\\ContratosRescindidos_22069_20231115-191427.xlsx']):
        if not isinstance(lista_arquivos, list):
            raise KeyError("apenas lista podem ser carregadas nesta classe")
        
        for arquivo in lista_arquivos:
            try:
                arquivo_exten = f".{arquivo.split('.')[-1:][0]}"
            except:
                continue

            if arquivo_exten in self.__exten_excel:
                app = xw.App(visible=False)
                wb = app.books.open(arquivo)
                #wb = xw.Book(arquivo)
                if len(wb.sheets) > 1:
                    wb.sheets[0].delete()

                caminho_temp = arquivo.split("\\")
                nome_arquivo = caminho_temp.pop(-1)
                caminho_temp = '\\'.join(caminho_temp)
                arquivo_temp = f"{caminho_temp}\\{datetime.now().strftime('%h %M')}temp.xlsx"

                nome_arquivo = nome_arquivo.split("_")
                nome_arquivo = nome_arquivo[0]

                wb.save(arquivo_temp)
                wb.close()
                for x in xw.apps:
                    x.quit()
                

                df = pd.read_excel(arquivo_temp)
                df.replace([float('inf'), float('-inf')], float('nan'), inplace=True)
                df = df.dropna()
                #arquivo_final = df.to_json()
                colunas = df.columns.tolist()
                arquivo_final = {}
                for coluna in colunas:
                    arquivo_final[coluna] = df[coluna].tolist()

                os.unlink(arquivo_temp)

                self.__dicionatio_final[nome_arquivo] = arquivo_final


        
        return self.__dicionatio_final

if __name__ == "__main__":
    tratar = ImobmeExceltoJson()
    arquivos = tratar.tratar_arquivos(['C:\\Projetos\\PatrimarAPI\\downloads\\ContratosRescindidos_22069_20231115-191427.xlsx'])
    arquivos = arquivos['ContratosRescindidos']['Código SPE']
    #print(arquivos)
    
    


    #for key in arquivos['ContratosRescindidos']:
    #    print(key)
            
                




# df = pd.read_excel(caminho)
# df = df.to_json()

# os.unlink(caminho)
# with open("TEST.json", 'w')as arqui:
#     arqui.write(df)