import pandas as pd

df= pd.DataFrame.from_csv('uasg.csv', encoding = "ISO-8859-1")
json_dict = []
count =0
for index, row in df.iterrows():
    count +=1
    obj = {
        "model": "myapp.person",
        "pk": count,
        "fields": {
            'codigo':index,
            'nome':row['Nome'],
            'uf':row['UF'],
        }
    }
    json_dict.append(obj)

f = open('uasgfixture.json','w')
f.write(str(json_dict))
f.close()
