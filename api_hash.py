import secrets
import json
import sys

class Hashs():
    def __init__(self):
        self.__arquivo_hash = 'hashs.json'
        try:
            with open(self.__arquivo_hash, 'r')as arqui:
                self.hash = json.load(arqui)
        except:
            default_hashs = {}
            with open(self.__arquivo_hash, 'w')as arqui:
                json.dump(default_hashs, arqui)
            self.hash = default_hashs
    
    def create_hash(self, nome):
        token = secrets.token_hex(64)
        self.hash[token] = {"nome" : nome, "permissão": 1}
        with open(self.__arquivo_hash, 'w')as arqui:
            json.dump(self.hash, arqui)

    def delete_hash(self, hash_to_del):
        try:
            del self.hash[hash_to_del]
            with open(self.__arquivo_hash, 'w')as arqui:
                json.dump(self.hash, arqui)
        except:
            print("-------------------- Erro ao Deletar Chave")
            print(f"{hash_to_del} não foi encontrado\n")



if __name__ == "__main__":
    while True:
        chave = Hashs()
        entrada = input("digite o comando: ")
        if entrada.lower() == "sair":
            sys.exit()
        elif entrada.lower() == "show":
            print("<-----chaves cadastradas----->")
            for key,value in chave.hash.items():
                print(f"usuario: {value['nome']} | chave: {key}")
            print()
        elif entrada.lower() == "add":
            nome = input("digite o Nome: ")
            chave.create_hash(nome)
        elif entrada.lower() == "del":
            hash_to_del = input("digite a hash para deletar: ")
            chave.delete_hash(hash_to_del)

        
