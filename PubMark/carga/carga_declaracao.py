# import pandas as pd
# from pymongo import MongoClient
# import pprint
#
# client = MongoClient('192.168.0.25', 27017)
# db = client['caranda']
# collectionUasg = db['forn_uasg']
# collectionFornecedor = db['forn_fornecedor']
#
# df= pd.read_csv('database_preg_2017.csv', delimiter=';', encoding="ISO-8859-1", dtype={'nu_cpfcnpj_fornecedor': str}, usecols=['co_uasg', 'nu_cpfcnpj_fornecedor', 'nu_pregao' ])
# print("csv importado")
#
# count = 0
# f = open('declaracaofixture.json', 'a')
#
# for index, row in df.iterrows():
#     count +=1
#
#     codUasg = row['co_uasg']
#     uasg = collectionUasg.find_one({"id": codUasg})
#
#     cnpj = str(row['nu_cpfcnpj_fornecedor'])
#     fornecedor = collectionFornecedor.find_one({"cnpj": cnpj})
#
#     # print("nada" + str(count/len(df)))
#     json_dict = []
#     if uasg is not None and fornecedor is not None:
#         # pprint(uasg)
#         # pprint(fornecedor)
#         obj = {
#             "model": "forn.pregao",
#             "pk": count,
#             "fields": {
#                 "numero": row['nu_pregao'],
#                 "id_uasg": row['co_uasg'],
#                 "id_fornecedor": fornecedor['id'],
#             }
#         }
#         json_dict.append(obj)
#     else:
#         print("note found" + str(codUasg) + " - " + str(cnpj))
#
#     cnpj = None
#     fornecedor = None
#     if count % 100 == 0:
#         print("progress:  " + str(count))
#
#     f.write(str(json_dict))
#
#
#
# f.close()
# print("acabou")

import json
import requests

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
offsetMax = j
pkCount = 1
fixtureCount = -1
while j <= offsetMax:

    #offset de 500 documentos por acesso
    offsetSize = 500
    offset = j*offsetSize

    # URL para acesso aos dados (usar offset para variar)
    url = 'http://compras.dados.gov.br/contratos/v1/contratos.json?offset=' + str(offset)
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

        if j == 0:
            # Pegando a quantidade de documentos
            collectionSize = int(s[-7:-1])
            print("qtd docs para download: " + str(collectionSize))
            offsetMax = int(collectionSize/500)

        # verifica se o offset transbordou a qtde de documentos ou se o servidor respondeu a requisicao sem sucesso
        if s[0] == '<':
            print("o servidor respondeu a requisicao sem sucesso")
            sucesso = bool(0)

    # verifica se o server respondeu a requisição com sucesso
    if sucesso:
        # Agora eu vou "quebrar" a string em uma lista de strings com o split"
        l = s.split('{"identificador"')


        # Removendo primeiro item  = cabeçalho
        l.pop(0)

        #Removendo 'resto' no ultimo item = contador de itens

        if j == 0:
            l[-1] = l[-1][:-17]
        else:
            l[-1] = l[-1][:-(27 + len(str(j*500)))]

        # adicionando '{"id"' que se perdeu no split
        l = ['{"identificador"'+i[:-1] for i in l]

        L = []  # lista final

        print("----------new offset: " + str(pkCount) + " - " + str(j) + " - " + str(j/offsetMax) + " Len:" + str(len(l)))

        fixtureSize = 10000
        if pkCount % fixtureSize == 1:
            fixtureCount += 1
            f = open('contratofixture (' + str(fixtureCount) + ').json', 'w')
        else:
            f = open('contratofixture (' + str(fixtureCount) + ').json', 'a')

        for i in l:
            jsonDict = json.loads(i)
            obj = {
                "model": "forn.contrato",
                "pk":  pkCount,
                "fields": jsonDict
                }
            L.append(obj)
            pkCount += 1

        print("start writing")
        f.write(json.dumps(L))
        f.close()
        print("finish writing")
        j += 1
    else:
        print("download failed, trying again")
