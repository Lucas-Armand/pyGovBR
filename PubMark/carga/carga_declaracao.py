import pandas as pd
from pymongo import MongoClient
import pprint

client = MongoClient('192.168.0.25', 27017)
db = client['caranda']
collectionUasg = db['forn_uasg']
collectionFornecedor = db['forn_fornecedor']

df= pd.read_csv('database_preg_2017.csv', delimiter=';',encoding="ISO-8859-1",dtype={'nu_cpfcnpj_fornecedor': str}, usecols=['co_uasg', 'nu_cpfcnpj_fornecedor', 'nu_pregao' ])
print("csv importado")

count = 0
f = open('declaracaofixture.json', 'a')

for index, row in df.iterrows():
    count +=1

    codUasg = row['co_uasg']
    uasg = collectionUasg.find_one({"id": codUasg})

    cnpj = str(row['nu_cpfcnpj_fornecedor'])
    fornecedor = collectionFornecedor.find_one({"cnpj": cnpj})

    # print("nada" + str(count/len(df)))
    json_dict = []
    if uasg is not None and fornecedor is not None:
        # pprint(uasg)
        # pprint(fornecedor)
        obj = {
            "model": "forn.pregao",
            "pk": count,
            "fields": {
                "numero": row['nu_pregao'],
                "id_uasg": row['co_uasg'],
                "id_fornecedor": fornecedor['id'],
            }
        }
        json_dict.append(obj)
    else:
        print("note found" + str(codUasg) + " - " + str(cnpj))

    cnpj = None
    fornecedor = None
    if count % 100 == 0:
        print("progress:  " + str(count))

    f.write(str(json_dict))



f.close()
print("acabou")


