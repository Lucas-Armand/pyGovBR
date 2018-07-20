import pandas as pd
import json
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

url = 'http://compras.dados.gov.br/fornecedores/v1/fornecedores.json?uf='
r = requests.get(url)
s = r.text
l = s.split('{"id"')
l.pop(0)  # Removendo primeiro item  = cabeçalho
l[-1] = l[-1][:-17] #Removendo 'resto' no ultimo item = contador de itens 
l = ['{"id"'+i[:-1] for i in l] # adicionando '{"id"' que se perdeu no split

count = 0
L = [] # lista final
for i in l:
    jsonDict = json.loads(i)
    obj = {
        "model": "forn.fornecedor",
        "pk": count,
        "fields": jsonDict
        }
    L.append(json.dumps(obj))
    count +=1]

f = open('fornfixture.json','w')
f.write(str(L))
f.close()

