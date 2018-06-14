# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:17:40 2018

@author: Lucas
"""


import pandas as pd
import requests
import json
from dateutil.parser import parse
import matplotlib.pyplot as plt

# Esse programa é uma tentativa de extruturar as informações da API do governo 
# federal de maneira orientada a objetos aonde os objetos são empresas


mypath = './database/database_preg_2017.csv'
if not 'DF' in globals():
    # Parte mais demorada do cod.
    DF = pd.read_csv(mypath, engine='python', error_bad_lines=False, sep=';')

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

def findUASG(uasgcod):    
    url = 'http://compras.dados.gov.br/licitacoes/doc/uasg/'+str(uasgcod)+'.json'
    r = requests.get(url)
    jsonDict = json.loads(r.text)
    jsonData = jsonReconstruct(jsonDict)
    return jsonData[0]

class Empresa(object):

    def __init__(self, cnpj):
        self.cnpj = cnpj
        self.df = DF
        self.attr = self.findAttr()


    def setAttr(self, attr):
        self.attr = attr

            
    def getAttr(self):
        return(self.attr)
                
                                                                                                                                                                                                                                                                                                     
    def findAttr(self, cnpj = None):
        if not cnpj:
            cnpj = self.cnpj
        # Pegandos dados da API:
        url = 'http://compras.dados.gov.br/fornecedores/doc/fornecedor_pj/'+str(cnpj)+'.json'
        r = requests.get(url)
        jsonDict = json.loads(r.text)
        jsonData = jsonReconstruct(jsonDict)
        return jsonData[0]
    
    def findPregoes(self):
        df = self.df
        cnpj = self.cnpj
        ### É possível mudar a forma de busca:
        ## Buscar pregoões pelo campo "link":
        #link = '/fornecedores/id/fornecedor_pj/'+str(cnpj)
        #DF = df.loc[df['_links']==link]
        ## Buscar pregões por nome:
        #DF.loc[df['fornecdor'].str.contains('COPACOL-COOPERATIVA AGROINDUSTRIAL')]
        ## Buscar pelo cpf:
        df_cnpj = df.loc[df['nu_cpfcnpj_fornecedor']==int(cnpj)]
        return df_cnpj
    
    def findRivals(self):
        concorrentes ={}
        df = self.df
        DF = self.findPregoes()
        # DF tem dados de todos os pregoes
        n_pregList = DF.nu_pregao.unique()
        for n_preg in n_pregList:
            # DF_nPre
            DF_nPreg = DF.loc[df['nu_pregao']==n_preg]
            uasgList = DF_nPreg.co_uasg.unique()
            for uasg in uasgList:
                DF_nPreg_uasg = df.loc[df['co_uasg']==uasg].loc[df['nu_pregao']==n_preg ]
                keys = concorrentes.keys()
                for row in DF_nPreg_uasg[['_links','fornecdor']].iterrows():
                    comp = row[1][1]
                    cnpj = row[1][0][-14:]
                    if comp in keys:
                        concorrentes[comp]['count']+= 1
                    else:
                        concorrentes[comp] = {'count':1,'cnpj':cnpj}
        df_conc = pd.DataFrame.from_dict(concorrentes,orient='index')
        if not df_conc.empty:
            df_conc = df_conc.sort_values(by=['count'], ascending=False)
        return df_conc
    
    def findContracts(self, dateMin = "2017-01-01", dateMax =  "2018-12-31"):
        cnpj = self.cnpj
        # Abrindo o site inicial do comprasnet para acessar o codigo do pregão #    
        url = 'http://compras.dados.gov.br/contratos/v1/contratos.json'
        parameters ={"cnpj_contratada": cnpj,
                     "data_inicio_vigencia_min":dateMin,
                     "data_inicio_vigencia_max":dateMax}
        r = requests.get(url, params= parameters)
        jsonDict = json.loads(r.text)
        jsonData = jsonReconstruct(jsonDict)
        df = pd.DataFrame(jsonData)
        if not df.empty:
            df = df.sort_values(by=['numero_processo'])
        return df
    
    def getIndex(self, dateMin = "2017-01-01", dateMax =  "2018-12-31"):
        index = {}
        # Indicadores de Pregões:
        df_preg = self.findPregoes()
        index['PREG_PARTICIPADOS'] = len(df_preg)
        
        df_cont = self.findContracts(dateMin,dateMax)
        if not df_cont.empty:
            print(df_cont)
            # Modalidade da Licitação : 5 = PREGÃO
            df_cont = df_cont.loc[df_cont['modalidade_licitacao'] == 5]
            # Só as de 2017
            df_cont = df_cont.loc[df_cont.licitacao_associada.str[-4:] == '2017']
            
        if not df_cont.empty:
            df_cont['duration']=df_cont[['data_inicio_vigencia','data_termino_vigencia']].apply(lambda x: (parse(x.data_termino_vigencia)-parse(x.data_inicio_vigencia)).days/365., axis=1)
            df_cont['valor_ano'] = df_cont['valor_inicial']/df_cont['duration']
            contratos = {}
            n_proc = df_cont.licitacao_associada.unique()
            for n in n_proc:
                df_proc = df_cont.loc[df_cont['licitacao_associada'] == n]
                contratos[n] = df_proc.valor_ano.sum()
            mediaPregao = pd.DataFrame.from_dict(contratos,orient='index')
            index['PREG_VENCIDOS'] = len(mediaPregao)
            index['PREG_VAL_ANO'] = 'R${:,.2f}'.format(mediaPregao[0].mean())
        else:
            index['PREG_VENCIDOS'] = 0
            index['PREG_VAL_ANO'] = 0
        # Indicadores de Contratos:
        if not df_cont.empty:
            df_cont = self.findContracts(dateMin='2013-01-01')
            df_cont['duration']=df_cont[['data_inicio_vigencia','data_termino_vigencia']].apply(lambda x: (parse(x.data_termino_vigencia)-parse(x.data_inicio_vigencia)).days/365., axis=1)
            df_cont['valor_ano'] = df_cont['valor_inicial']/df_cont['duration']
            df_cont['orgao']=df_cont['uasg'].apply(lambda x:findUASG(x)['nome'])
            index['CONT_N'] = len(df_cont) 
            index['CONT_VAL_ANO'] = 'R${:,.2f}'.format(df_cont.valor_ano.mean())
            try:
                index['CONT_ADIT_N'] = "%.1f" % df_cont.numero_aditivo.mean()
            except:
                index['CONT_ADIT_N'] = 0
                pass
                
        else:
            index['CONT_N'] = 0
            index['CONT_VAL_ANO'] = 0
            index['CONT_ADIT_N'] = 0
            
            
        return(index,df_cont,df_preg)
    
    def getIndexRivals(self,N=5):
        rivals = self.findRivals()
        count=0
        IDX =[]
        for index, row in rivals.iterrows():
            cnpj = row['cnpj']
            empr = Empresa(cnpj)
            name = empr.attr['razao_social']
            index,df_cont,df_preg = empr.getIndex()
            index['CNPJ'] = empr.cnpj
            index['N_CONCORRENCIAS'] = row['count']
            IDX.append({name:index})
            print(' - - > '+str(count)+ ' / '+str(N))
            if count>N:
                break
            count+=1
        return IDX
        
def piechart(bsns,n=10):
    
    # PIE CHART TOP 10 CLIENTES
    index,df_cont,df_preg = bsns.getIndex()
    hist = df_cont.orgao.value_counts()
    count=[]
    keys = hist.keys()
    i = 0
    for k in keys:
        i+=1
        if i<=n+1:
            count.append(hist[k])
        else:
            #Somando todo o resto no 11° slot
            count[n]+=hist[k]
            
    fig1, ax1 = plt.subplots()
    if i<=n:
        ax1.pie(count, labels=keys, autopct='%1.1f%%',
                shadow=True, startangle=90)
    else:
        ax1.pie(count, labels=list(keys[0:n])+['OUTROS'], autopct='%1.1f%%',
                shadow=True, startangle=90)
        
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
    
    
def chartCONTRATO(bsns,n=10):
    index,df_cont,df_preg = bsns.getIndex()
    # HOISTOGRAM ORIGEM CONTRATO 
    df_cont['modalidade_licitacao2']=df_cont['modalidade_licitacao'].apply(lambda x: 'LICITAÇÃO' if x==5  else 'DISPENSA')
    df_cont['modalidade_licitacao2'].hist()
    
    
    
def chartLICITACAO(bsns,n=10):
    index,df_cont,df_preg = bsns.getIndex()
    # HOISTOGRAM ANO LICITAÇÃO
    df_cont['data_inicio_vigencia'].str[0:4].hist()
 
def main():
    bsns = Empresa(39818737000151)
    attr = bsns.attr
    index,df_cont,df_preg = bsns.getIndex()
    print('# Atributos da empresa:')
    print(attr)
    print('')
    print('# Resultados empresa:')
    print(index)
    print('')
    print('# Resumo banco de dados dos contratos:')
    print(df_cont.head())
    print('')
    print('# Resumo banco de dados dos Pregões:')
    print(df_preg.head())
    print('')
    print('# Graficos:')
    piechart(bsns)
    chartLICITACAO(bsns)
    chartCONTRATO(bsns)

if __name__ == '__main__':
    show = False
    if show:
        main()
                                            
