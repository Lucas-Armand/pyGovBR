import pandas as pd
import json

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

# URL para acesso aos dados (usar offset para variar)
url = 'http://compras.dados.gov.br/fornecedores/v1/fornecedores.json?uf='

# Fazendo o request do servidor
r = requests.get(url)

# O resultado é guardado como uma string(s) 
s = r.text

# Agora eu vou "quebrar" a string em uma lista de strings com o split"
l = s.split('{"id"')

# Removendo primeiro item  = cabeçalho
l.pop(0)  

#Removendo 'resto' no ultimo item = contador de itens 
l[-1] = l[-1][:-17]

# adicionando '{"id"' que se perdeu no split
l = ['{"id"'+i[:-1] for i in l]

# Agora vou iniciar um loop para editar essas strings
count = 0
L = [] # lista final
for i in l:
    jsonDict = json.loads(i)
    obj = {
        "model": "forn.fornecedor",
        "pk": count,
        "fields": jsonDict
        }
    L.append(obj)
    count +=1

f = open('fornfixture.json','w')
f.write(json.dumps(L))
f.close()

