import pandas as pd
from pymongo import MongoClient
import pprint

client = MongoClient('localhost', 27017)
db = client['caranda']
collectionUasg = db['forn_uasg']
collectionFornecedor = db['forn_fornecedor']

df= pd.read_csv('database_preg_2017.csv', delimiter=';',encoding="ISO-8859-1")
print("csv importado")
json_dict = []
count = 0

for index, row in df.iterrows():
    count +=1

    uasg = collectionUasg.find_one({"codigo": row['co_uasg']});
    fornecedor = collectionFornecedor.find_one({"cnpj": row['nu_cpfcnpj_fornecedor']})

    print("nada" + str(count/len(df)))
    if uasg is not None and fornecedor is not None:
        pprint(uasg)
        pprint(fornecedor)
        obj = {
            "model": "forn.pregao",
            "pk": count,
            "fields": {
                'numero': row['nu_pregao'],
                'id_uasg': uasg['id'],
                'id_fornecedor': fornecedor['id'],
            }
        }
        json_dict.append(obj)

#f = open('uasgfixture.json','w')
f = open('pregaofixture.json','w')
f.write(str(json_dict))
f.close()
