# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 15:48:14 2018

@author: Lucas
"""
import os
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


# Aparentemente tem um erro nesse programa, quando tem grupos eu não pego as 
# discrições dos itens e as vezes tem várias paginas tbm n funciona.
def findUASG(cod = None, name = None):
    # Essa função busca no banco de dados de UASG por nome ou número e retorna 
    # o resultado
    
    # pegando os dados dos uasg dos bancos de dados 
    df = pd.read_csv('./database/uasg.csv', engine='python', error_bad_lines=False, sep=';')
    
    # Se o usuário entra com um código ele procura o uasg desse codigo
    if cod!= None:
        # busca exatamente o codigo entrado (deve ser int!)
        result = df.loc[df['Código']==cod]
    elif name!= None:
        # busca por nomes no banco de dados que contenham o nome input
        result = df.loc[df['Nome'].str.contains(name.upper())]
    else:
        # caso não exista entrada ele retorna um dataframe vazio
        result = pd.DataFrame(None)
    # retornando o resultado da pesquisa
    return(result)
    
class UASG(object):
    """
    Classe UASG (Unidade Adiministradora de Serviços do Governo) é a classe 
    de objetos referentes aos dados disponiveis sobre uma determinada uasg,
    o objetivo dessa classe é levantar dados sobre os pregões e contratos 
    realizados por uma unidade e, com isso buscar, padrões na atividade da 
    unidade.
    """
    def __init__(self, cod):
        # O objeto UASG recebe só o codigo e utiliza essa informação para defenir 
        # os outros parâmetros, evitando que o usuário tenha que faze-lo manual
        r = findUASG(cod)
        self.cod = cod 
        self.name = r.Nome.tolist()[0]
        self.uf = r.UF.tolist()[0]
                  
    def findPregoes(self):
        # Essa função gera duas saidas:
        # * self.resumo_pregoes : um resumo de cada pregão realizado no periodo
        # * self.intens_pregoes : dados de todos os itens apregoados pela unidade
        # Essa função busca as informações na base de dados local, caso não exista
        # ele pergunta se usuário quer importar os dados da comprasnet - TEMPO!!!
        
        # Definições iniciais
        cod = self.cod      # codigo do uasg 
        
        #Buscando na base de dados
        for file in os.listdir("./database/uasgs/"):
            if file.split(' - ')[0] == str(cod):
                filepath = './database/uasgs/'+file
                self.pregoes = pd.read_csv(filepath+'/pregoes.csv', 
                                                  engine='python', 
                                                  error_bad_lines=False, 
                                                  sep=';')
                break
    
        # Teste se o loop chegou até o final sem achar resultado
        if file == 'desktop.ini':
            #Nesse caso devese importar os valores do portal "comprasnet"
            answer = input("Não foram encontradas as informações dessa UASG no"+
                           "repositório de dados estáticos.\n"+ 
                           "Você deseja importar os dados da unidade?\n"+
                           "(ATENÇÃO ESSA OPÇÃO PODE DEMANDAR ALGUNS MINUTOS!)"+
                           "[Y/N]")
            if answer.upper() == 'Y':
                
                ## Levantando pregões participados
                # Abrindo o site inicial do comprasnet para acessar o codigo dos pregões #
                
                # Pregões eletrônicos:
                url = 'http://comprasnet.gov.br/livre/pregao/ata4.asp'
                parameters ={"co_uasg":cod,
                             "rdTpPregao": "E"}
                r = requests.get(url, params= parameters)
                soup = BeautifulSoup(r.text, "html.parser")
                pattern = re.compile("\r\n([0-9]*)")
                matchs = pattern.findall(soup.text)
                
                # Pregões presenciais:
                parameters ={"co_uasg":cod,
                             "rdTpPregao": "P"}
                r = requests.get(url, params= parameters)
                soup = BeautifulSoup(r.text, "html.parser")
                pattern = re.compile("\r\n([0-9]*)")
                matchs += pattern.findall(soup.text)
                
                # Filtrando informações anteriores a 2010
                filt = []
                for preg_cod in matchs:
                    if int(preg_cod[-4:])>=2010:
                        filt.append(preg_cod)
                matchs = filt
                
                ## Levantando os dados dos pregão 
                data= []
                for preg_cod in matchs:
                    # Imprimir o codigo do pregao para o usuário acompanhar o avanço
                    print(preg_cod)
                    url = 'http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Relacao.asp'
                    parameters ={"numprp":preg_cod,
                                 "txtlstUasg": cod}
                    r = requests.get(url, params= parameters)
                    soup = BeautifulSoup(r.text, "html.parser")
                    soup.text
                    pattern = re.compile( "Objeto:\xa0(.*)"+
                                          "Edital a partir de:\xa0(.*)"+
                                          "Endereço:\xa0(.*)"+
                                          "Telefone:\xa0(.*)"+
                                          "Fax:\xa0(.*)"+
                                          "Entrega da Proposta:\xa0(.*)"+
                                          "Abertura da Proposta:\xa0(.*)")
                    # O resultado esperado é um lista de um unico objeto que 
                    # tem todo os itens a cima em sequencia
                    match = pattern.findall(soup.text)
                    
                    # Caso o pregão exista no endereço:
                    if match:
                        # Estruturando dados do resumo do pregão:
                        preg = {'preg_cod':preg_cod,
                                'Objeto':match[0][0],
                                'Edital':match[0][1],
                                'Endereço':match[0][2],
                                'Telefone':match[0][3],
                                'Fax':match[0][4],
                                'Entrega da Proposta':match[0][5],
                                'Abertura da Proposta':match[0][6]}
                        # Salvando dados de cada pregão
                        data.append(preg)
                    
                # Construindo dataframe final1
                df = pd.DataFrame.from_dict(data)
                
                # Salvando dataframe para consultas futuras
                # Criando a pasta:
                name = self.name.split('\\')[0]
                filename = str(cod)+' - '+name
                filepath = './database/uasgs/'+filename
                os.makedirs(filepath)
                # Criando arquivo csv:
                df.to_csv(filepath+'/pregoes.csv', sep =';')
                
                # Armazendo o resutado com um parametro do obj. UASG
                self.pregoes = df
                
            
            
            
            
                #http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Relacao.asp?numprp=12013&txtlstUasg=201014
                #http://comprasnet.gov.br/livre/pregao/ata4.asp?rdTpPregao=E&co_uasg=201014
# =============================================================================
#                 
#                 
#                 for ano in ['2012','2013','2014']:
#                     cont = 0
#                     while True:
#                         cont+=1
#                         key =  str(cont)+ano
#                         
#                         # Abrindo o site inicial do comprasnet para acessar o codigo do pregão #    
#                         url =  'http://comprasnet.gov.br/livre/pregao/ata2.asp?co_no_uasg=986001&numprp='+key+'&f_lstSrp=&f_Uf=&f_numPrp=82013&f_codUasg=986001&f_tpPregao=E&f_lstICMS=&f_dtAberturaIni=&f_dtAberturaFim='
#                         r = requests.get(url)
#                         data = r.text
#                         soup = BeautifulSoup(data, "html.parser")
#                         pattern = re.compile(r'prgcod=([0-9]+)+";', re.MULTILINE | re.DOTALL)
#                         script = soup.find("script", text=re.compile(r'url\ ='))
#                         if script:
#                             match = pattern.search(script.text)
#                             if match:
#                                 prgcod = match.group(1) # acesando código do pregão
#                         #####################################################################
#                         
#                         
#                         if not prgcod == '0':   # Isso significa que a licitação análisada n existe.
#                         
#                             # Acessando a pagina de itens do pregão
#                             url = 'http://comprasnet.gov.br/livre/pregao/termojulg.asp'
#                             parameters ={"prgcod": prgcod,
#                             "Acao": "A",
#                             "co_no_uasg": "986001", # Mun. Rio UASG
#                             "numprp": key,
#                             "f_lstSrp": None,
#                             "f_Uf": None,
#                             "f_numPrp": key,
#                             "f_coduasg": "986001",
#                             "f_tpPregao": "E" ,      # Sempre 'E' (mas n faz diferença)
#                             "f_lstICMS": None,
#                             "f_dtAberturaIni": None,
#                             "f_dtAberturaFim": None}
#                             
#                             r = requests.get(url, params= parameters)
#                             data = r.text
#                             soup = BeautifulSoup(data, "html.parser")
#                             item = 0
#                             for cell in soup.find_all('td'):
#                                 if 'colspan'  or 'width' in cell.attrs.keys():
#                                     text = cell.getText()
#                                     text = re.sub('\\n','',text)
#                                     text = re.sub('\\t','',text)
#                                     if ':' in text:    
#                                         element = re.split(': |, ',text)
#                                         if element[0] == 'Descrição': # primeiro tópíco
#                                             item = {'Licitação':str(cont),
#                                                     'Ano':ano,
#                                                     'chave':key,
#                                                     'prgcod':prgcod,
#                                                     'url':url,
#                                                     element[0]:element[1]}
#                                         if item !=0: # Isso seguinifica que já encontramos uma "Discrição"
#                                             if len(element) == 2:
#                                                 item[element[0]]=element[1]
#                                             else:
#                                                 if element[0] == 'Adjudicado para':
#                                                     item[element[0]]=element[1]
#                                                     for e in element:
#                                                         pattern1 = re.compile('pelo\smelhor\slance\sde\sR\$\s([\d\.]*\,\d{1,2})', re.MULTILINE | re.DOTALL)
#                                                         pattern2 = re.compile('com\svalor\snegociado\sa\sR\$\s([\d\.]*\,\d{1,2})', re.MULTILINE | re.DOTALL)
#                                                         match1 = pattern1.search(e)
#                                                         match2 = pattern2.search(e)
#                                                         if pattern1.search(e):
#                                                             item['Melhor Lance'] = match1.group(1) 
#                                                         if pattern1.search(e):
#                                                             item['Valor Negociado'] = match1.group(1) 
#                                                     print(item)
#                                                     Data.append(item)
#                         if cont>900:
#                             break
#                         
#         
#             else:
#                 print('As informações não foram importadas')
#                 print('Não foi possivel construir os dataframes!')
#             
# =============================================================================
        
        
        
        
        
# =============================================================================
#     def findRivals(self):
# 
#         return df_conc
#     
#     def findContracts(self, dateMin = "2017-01-01", dateMax =  "2018-12-31"):
# 
#         return df
#     
#     def getIndex(self, dateMin = "2017-01-01", dateMax =  "2018-12-31"):
# 
#         return(index,df_cont,df_preg)
#     
#     def getIndexRivals(self,N=5):
# 
#         return IDX
# =============================================================================


# =============================================================================
# 
# 
# 
# 
# Data = []
# 
# for ano in ['2012','2013','2014']:
#     cont = 0
#     while True:
#         cont+=1
#         key =  str(cont)+ano
#         
#         # Abrindo o site inicial do comprasnet para acessar o codigo do pregão #    
#         url =  'http://comprasnet.gov.br/livre/pregao/ata2.asp?co_no_uasg=986001&numprp='+key+'&f_lstSrp=&f_Uf=&f_numPrp=82013&f_codUasg=986001&f_tpPregao=E&f_lstICMS=&f_dtAberturaIni=&f_dtAberturaFim='
#         r = requests.get(url)
#         data = r.text
#         soup = BeautifulSoup(data, "html.parser")
#         pattern = re.compile(r'prgcod=([0-9]+)+";', re.MULTILINE | re.DOTALL)
#         script = soup.find("script", text=re.compile(r'url\ ='))
#         if script:
#             match = pattern.search(script.text)
#             if match:
#                 prgcod = match.group(1) # acesando código do pregão
#         #####################################################################
#         
#         
#         if not prgcod == '0':   # Isso significa que a licitação análisada n existe.
#         
#             # Acessando a pagina de itens do pregão
#             url = 'http://comprasnet.gov.br/livre/pregao/termojulg.asp'
#             parameters ={"prgcod": prgcod,
#             "Acao": "A",
#             "co_no_uasg": "986001", # Mun. Rio UASG
#             "numprp": key,
#             "f_lstSrp": None,
#             "f_Uf": None,
#             "f_numPrp": key,
#             "f_coduasg": "986001",
#             "f_tpPregao": "E" ,      # Sempre 'E' (mas n faz diferença)
#             "f_lstICMS": None,
#             "f_dtAberturaIni": None,
#             "f_dtAberturaFim": None}
#             
#             r = requests.get(url, params= parameters)
#             data = r.text
#             soup = BeautifulSoup(data, "html.parser")
#             item = 0
#             for cell in soup.find_all('td'):
#                 if 'colspan'  or 'width' in cell.attrs.keys():
#                     text = cell.getText()
#                     text = re.sub('\\n','',text)
#                     text = re.sub('\\t','',text)
#                     if ':' in text:    
#                         element = re.split(': |, ',text)
#                         if element[0] == 'Descrição': # primeiro tópíco
#                             item = {'Licitação':str(cont),
#                                     'Ano':ano,
#                                     'chave':key,
#                                     'prgcod':prgcod,
#                                     'url':url,
#                                     element[0]:element[1]}
#                         if item !=0: # Isso seguinifica que já encontramos uma "Discrição"
#                             if len(element) == 2:
#                                 item[element[0]]=element[1]
#                             else:
#                                 if element[0] == 'Adjudicado para':
#                                     item[element[0]]=element[1]
#                                     for e in element:
#                                         pattern1 = re.compile('pelo\smelhor\slance\sde\sR\$\s([\d\.]*\,\d{1,2})', re.MULTILINE | re.DOTALL)
#                                         pattern2 = re.compile('com\svalor\snegociado\sa\sR\$\s([\d\.]*\,\d{1,2})', re.MULTILINE | re.DOTALL)
#                                         match1 = pattern1.search(e)
#                                         match2 = pattern2.search(e)
#                                         if pattern1.search(e):
#                                             item['Melhor Lance'] = match1.group(1) 
#                                         if pattern1.search(e):
#                                             item['Valor Negociado'] = match1.group(1) 
#                                     print(item)
#                                     Data.append(item)
#         if cont>900:
#             break
# =============================================================================




# =============================================================================
#         
# 
# 
# url0 = 'http://www.fazenda.rj.gov.br/tfe/web/contrato'
# r0  = requests.get(url0)  # Acessando o site
# c = r0.cookies
# print(c)
# time.sleep(5)
# 
# values = []
# for index in contratos:
#     url = 'http://www.fazenda.rj.gov.br/tfe/web/contrato/execucao?contrato='+index
#     r  = requests.get(url, cookies = c)  # Acessando o site
#     data = r.text           # Extraindo cod. HTML da pag.
#     soup = BeautifulSoup(data)  # transformando em um objeto Soup
#     info = [0,0,0]                  # Lista de informações importantes
#     
#     cont=0
#     for cell in soup.find_all('td'):    # Acessando as células da tabela da pag.
#         text = cell.getText()
#         if ',' in text:
#             # cada linha contem 3 valores com "," 
#             # esses são os três valores, respectivamente, são:
#             # Valor Empenhado	Valor Liquidado	Valor Pago
#             valueString = text
#             valueString = re.sub('\.','',valueString)   # tirando "."
#             valueString = re.sub(',','.',valueString)   # substituindo "," por "."
#             try:
#                 value = float(valueString)
#                 info[cont]+=value
#                 cont+=1
#             except:
#                 pass
#         if cont==3:
#             cont = 0
#     values.append(info)
#     print(info)
# 
# data={'ano': '2018',
# 'codigoUg': '',
# 'codigoSituacao':'' ,
# 'codigoModalidade': '6',
# 'cpf': '',
# 'cnpj': '',
# 'nomeContratada': '',
# 'codigoContrato':'', 
# 'captcha': 'M7TQ'}
# 
# =============================================================================

