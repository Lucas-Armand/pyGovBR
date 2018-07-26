
# import from csv outdated
#import pandas as pd


# df= pd.read_csv('uasg.csv', encoding = "ISO-8859-1")
# json_dict = []
# count =0
# for index, row in df.iterrows():
#     count +=1
#     obj = {
#         "model": "forn.uasg",
#         "pk": count,
#         "fields": {
#             'codigo':index,
#             'nome':row['Nome'],
#             'uf':row['UF'],
#         }
#     }
#     json_dict.append(obj)
#
# f = open('uasgfixture.json','w')
# f.write(str(json_dict))
# f.close()

from _codecs import latin_1_encode

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





j=0
docCount=1
count = j*500 + 1
while j < docCount:
    f = open('uasgfixture.json', 'a')

    # URL para acesso aos dados (usar offset para variar)
    url = 'http://compras.dados.gov.br/licitacoes/v1/uasgs.json?offset=' + str(j*500)
    print(url)

    # Fazendo o request do servidor
    sucesso = bool(1)
    sucessoRequest = bool(1)
    try:
        r = requests.get(url)
    except requests.exceptions.Timeout:
        print('timeout')
        sucessoRequest = bool(0)
    except requests.exceptions.ConnectionError:
        print('verifique conexão com a internet')
        sucessoRequest = bool(0)

    if sucessoRequest:
        # O resultado é guardado como uma string(s)
        s = r.text

        if(j==0):
            # Pegando a quantidade de documentos
            docCount = int(s[-6:-1])

        # verifica se o offset transbordou a qtde de documentos ou se o servidor respondeu a requisicao sem sucesso
        if s[0] == '<':
            print("o servidor respondeu a requisicao sem sucesso")
            sucesso = bool(0)

    # verifica se o server respondeu a requisição com sucesso
    if sucesso:
        # Agora eu vou "quebrar" a string em uma lista de strings com o split"
        l = s.split('{"id"')


        # Removendo primeiro item  = cabeçalho
        l.pop(0)

        #Removendo 'resto' no ultimo item = contador de itens

        if j == 0:
            l[-1] = l[-1][:-16]
        else:
            l[-1] = l[-1][:-(26 + len(str(j*500)))]

        # adicionando '{"id"' que se perdeu no split
        l = ['{"id"'+i[:-1] for i in l]

        L = []  # lista final

        print("----------new offset:" + str(count) + " - " + str(j) + " - " + str(j/784) + " Len:" + str(len(l)))
        print(l[499])
        for i in l:
            jsonDict = json.loads(i)
            obj = {
                "model": "forn.uasg",
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