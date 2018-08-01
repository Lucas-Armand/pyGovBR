from _codecs import latin_1_encode

import pandas as pd
import json
import requests
import pprint

# Esse método recebe um dicionário e transforma em uma lista
def jsonReconstruct(jsonDict):
    keys =  jsonDict.keys()
    if '_embedded' in keys:
        jsonList =  jsonDict['_embedded']['contratos']
        if jsonList:
            for json_ in jsonList:
                del json_['_links']
    elif '_links' in keys:
        keys = jsonDict['_links'].keys()
        for k in keys:
            jsonDict[k]=jsonDict['_links'][k]['title']
        del jsonDict['_links']
        jsonList = [jsonDict]
    return(jsonList)

# Agora vou iniciar um loop para editar essas strings





j=207
count = j*500 + 1
while j < 784:
    f = open('fornfixture.json', 'a')

    # URL para acesso aos dados (usar offset para variar)
    url = 'http://compras.dados.gov.br/fornecedores/v1/fornecedores.json?offset=' + str(j*500)
    print(url)

    # Fazendo o request do servidor
    r = requests.get(url)

    # O resultado é guardado como uma string(s)
    s = r.text

    # verifica se o offset transbordou a qtde de documentos
    if s[1] == 'h':
        break

    #verifica se o server respondeu a requisição com sucesso
    if s[1] != '!':
        # Agora eu vou "quebrar" a string em uma lista de strings com o split"
        l = s.split('{"id"')

        # Removendo primeiro item  = cabeçalho
        l.pop(0)

        #Removendo 'resto' no ultimo item = contador de itens

        if j == 0:
            l[-1] = l[-1][:-17]
        else:
            l[-1] = l[-1][:-(27 + len(str(j*500)))]

        # adicionando '{"id"' que se perdeu no split
        l = ['{"id"'+i[:-1] for i in l]

        L = []  # lista final

        print("----------new offset:" + str(count) + " - " + str(j) + " - " + str(j/784) + " Len:" + str(len(l)))

        for i in l:
            jsonDict = json.loads(i)
            obj = {
                "model": "forn.fornecedor",
                "pk":  count,
                "fields": jsonDict
                }
            L.append(obj)
            count += 1
        print("start writing")
        f.write(json.dumps(L))
        f.close()
        print("finish writing")
        j += 1
    else:
        print("download failed, trying again")