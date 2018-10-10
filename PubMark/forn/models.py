from djongo import models
import locale
locale.setlocale( locale.LC_ALL, '' )



UF_LIST = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amap√°'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Cear√°'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espirito Santo'),
        ('GO', 'Goi√°s'),
        ('MA', 'Maranh√£o'),
        ('MS', 'Mato Grosso do Sul'),
        ('MT', 'Mato Grosso'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Par√°'),
        ('PB ', 'Para√≠ba'),
        ('PR', 'Paran√°'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piau√≠'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rond√¥nia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'S√£o Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
        )

MODALIDADE_LICITACAO_LIST = {
        None:"Desconhecido",
        1:"CONVITE",                                                          
        2:"TOMADA DE PRECOS",                                                 
        3:"CONCORRENCIA",                                                     
        4:"CONCORRENCIA INTERNACIONAL",                                       
        5:"PREGAO",                                                           
        6:"DISPENSA DE LICITACAO",                                            
        7:"INEXIGIBILIDADE DE LICITACAO",                                     
        20:"CONCURSO",                                                        
        22:"TOMADA DE PRECOS POR TECNICA E PRECO",                            
        33:"CONCORRENCIA POR TECNICA E PRECO",                                
        44:"CONCORRENCIA INTERNACIONAL POR TECNICA E PRECO",                  
        99:"RDC",                                                             
        }

CEP_ESTADO = {
        20000:"S√£o Paulo",
        29000:"Rio de Janeiro",
        30000:"Espirito Santo",
        40000:"Minas Gerais",
        49000:"Bahia",
        50000:"Sergipe",
        57000:"Pernambuco",
        58000:"Alagoas",
        59000:"Para√≠ba",
        60000:"Rio Grande do Norte",
        64000:"Cear√°",
        65000:"Piau√≠",
        66000:"Maranh√£o",
        68900:"Par√°",
        69300:"Amazonas",
        69400:"Amap√°",
        69900:"Roraima",
        70000:"Acre",
        74000:"Distrito Federal",
        76800:"Mato Grosso",
        77000:"Goi√°s",
        78000:"Tocantins",
        79000:"Rond√¥nia",
        80000:"Mato Grosso do Sul",
        88000:"Paran√°",
        90000:"Santa Catarina",
        100000:"Rio Grande do Sul",
        }

ESTADOS = ["Acre","Alagoas","Amap√°","Amazonas","Bahia","Cear√°","Distrito Federal","Espirito Santo","Goi√°s","Maranh√£o","Mato Grosso","Mato Grosso do Sul","Minas Gerais","Par√°","Para√≠ba","Paran√°","Pernambuco","Piau√≠","Rio de Janeiro","Rio Grande do Norte","Rio Grande do Sul","Rond√¥nia","Roraima","Santa Catarina","S√£o Paulo","Sergipe","Tocantins"]
 

class Uasg(models.Model):
    id = models.ObjectIdField()
    nome = models.CharField(max_length=200)
    id_orgao = models.IntegerField(blank=True, null=True)
    id_municipio = models.IntegerField(blank=True, null=True)
    cep = models.CharField(max_length=20)
    total_fornecedores_cadastrados = models.IntegerField(blank=True, null=True)
    total_fornecedores_cadastrados = models.IntegerField(blank=True, null=True)
    unidade_cadastradora = models.BooleanField(default=False)
    ativo = models.BooleanField(default=False)
    #uf = models.CharField(max_length=3, choices=UF_LIST)
    # essa linha de cima faz um erro muito louco

    def uf(self):
        prefixo = int(self.cep[0:-3])
        keys = CEP_ESTADO.keys()
        for cep_test in keys:
            if prefixo<cep_test:
                return(CEP_ESTADO[cep_test])
        return(None)


class UasgManager(models.Manager):
    def create_uasg(self, id, nome):
        book = self.create(title=title)
        # do something with the book
        return book


class Fornecedor(models.Model):
    id = models.ObjectIdField()
    cnpj = models.CharField(max_length=20)
    #cpf = models.CharField(max_length=20, null=True)
    nome = models.CharField(max_length=200)
    ativo = models.BooleanField(default=False)
    recadastrado = models.BooleanField(default=False)
    id_municipio = models.IntegerField(blank=True, null=True)
    uf = models.CharField(max_length=3, choices=UF_LIST)
    id_natureza_juridica = models.IntegerField(blank=True, null=True)
    id_porte_empresa = models.IntegerField(blank=True, null=True)
    id_ramo_negocio = models.IntegerField(blank=True, null=True)
    id_cnae = models.IntegerField(blank=True, null=True)
    id_unidade_cadastradora = models.IntegerField(blank=True, null=True)
    habilitado_licitar = models.BooleanField(default=False)

    def filter_declaracao(self):
        return list(Declaracao.objects.filter(id_fornecedor = self.id))

    def filter_rival(self):
        # Essa func„o retorna um dicionario com todos os fornecedores que ja
        # competiram com 'self' em algum pregao. O dicion·rio È estruturado
        # por:
            # count -> N˙mero de vezes que a empresa concorreu com "self"
            # obj -> Que È o objeto fornecedor relacionado · empresa

        # Construimos uma lista com todas as declaracoes de participacao de
        # pregao de self:
        declaracoes = self.filter_declaracao()

        # Construimos a variavel dicionario "concorrentes" que sera o output
        concorrentes = {}
        for declaracao in declaracoes: # Para cada declaracao/pregao:
            # Construimos uma lista concorrentes naquele pregao:
            concorrentes_nesse_pregao = declaracao.filter_fornecedor_mesmo_pregao()
            for concorrente in concorrentes_nesse_pregao: # Para cada concorrente:
                # Reservamos o nome:
                nome = concorrente.nome
                
                if nome in concorrentes.keys(): # Se o nome ja foi adicionado:
                    # Isso significa que ja iniciado um contador em
                    # "concorretens, logo, devemos adicionar uma unidade ao
                    # contador :
                    concorrentes[nome]['count']+=1
                else:   # Se nao:                                          
                    # deve-se alocar espaco para o contador e para o objeto
                    # no dicionario:
                    concorrentes[nome]={}
                    concorrentes[nome]['count']=1
                    concorrentes[nome]['obj']=concorrente
        return concorrentes

    def filter_contrato(self):       
        # Essa func„o retorna uma lista de objetos "Contrato" com todos os
        # contratos relacionado ao cnpj de "self"

        cnpj = self.cnpj
        contratos = list(Contrato.objects.filter(cnpj_contratada = cnpj))
        return contratos

    def indicadores(self):
        # Esse mÈtodo retorna um dicion·rio com os principais indicadores sobre
        # participaÁ„o de licitaÁıes e contratos de self.

        # Acessando dados:
        declaracoes = self.filter_declaracao()
        contratos = self.filter_contrato()

        ### Processando dados
        
        # Contagem do n˙mero de pregıes participados:
        n_pregoes_participados = len(declaracoes)
        
        # Calculando numero de pregoes vencidos:
        codigo_pregoes_participados = [declaracao.numero for declaracao in declaracoes]
        contagem_pregoes_vencidos = 0
        for contrato in contratos:
            if contrato.numero_aviso_licitacao in codigo_pregoes_participados:
                contagem_pregoes_vencidos += 1

        # Calculo do valor mÈdio dos contratos:
        valores_dos_contratos = [contrato.valor_inicial if contrato.valor_inicial!= None else 0 for contrato in contratos]
        if len(contratos)>0:
            valor_medio_contratos = sum(valores_dos_contratos)/len(contratos)
        else:
            valor_medio_contratos = 0

        # Calculando a frequencia de contratos por ano:
        contratos_por_ano = []
        ano_contratos = [contrato.data_assinatura.year for contrato in contratos]
        anos = set(ano_contratos)
        anos = sorted(anos)
        for ano in anos:
            contratos_por_ano.append({
                'ano':ano,
                'contratos':ano_contratos.count(ano)
                })

        # Calculando numero medio de contratos por ano (media de todos anos):
        n = len(anos)
        media_n_contratos = sum([n_contratos_por_ano['contratos'] for n_contratos_por_ano in contratos_por_ano])/n

        # Calculando a duracao media dos contratos em meses
        #DURACAO MEDIA DOS CONTRATOS (MES)
        delta_tempo_contratos = []
        for contrato in contratos:
            delta_tempo_contratos.append(
                    contrato.data_termino_vigencia -
                    contrato.data_inicio_vigencia
                    )
        delta_tempo_contratos = [delta.days/30 for delta in delta_tempo_contratos]
        delta_tempo_contratos = sum(delta_tempo_contratos)/len(delta_tempo_contratos)

        
        # Calculando a frequencia das modalidades de licitaÁ„o dos contratos:
        contratos_por_modalidade = []
        modalidade_contratos = [contrato.modalidade_licitacao for contrato in contratos]
        modalidades = set(modalidade_contratos)
        for modalidade in modalidades:
            contratos_por_modalidade.append({
                'modalidade':MODALIDADE_LICITACAO_LIST[modalidade],
                'contratos':modalidade_contratos.count(modalidade)
                })


        # Calculando a frequencia de contratos por uasg:
        contratos_por_uasg = {}
        uasg_contratos = [contrato.uasg.nome for contrato in contratos]
        uasgs = set(uasg_contratos)
        for uasg in uasgs:
            contratos_por_uasg[uasg] = uasg_contratos.count(uasg)
        sorted_contratos_por_uasg = sorted(contratos_por_uasg.items(), key=lambda kv: kv[1], reverse=True)
        n = len(sorted_contratos_por_uasg)
        name = []
        count = []
        alfa = 0
        N = 5 # numero de uasg apresentados (arbitrario)
        for i in range(n):
            if i < N:
                name.append(sorted_contratos_por_uasg[i][0])
                count.append(sorted_contratos_por_uasg[i][1])
            else:
                alfa += sorted_contratos_por_uasg[i][1]
        if alfa != 0:
            name.append('Outros')
            count.append(alfa)
        sorted_contratos_por_uasg_extruturado = {}
        sorted_contratos_por_uasg_extruturado['name'] = name
        sorted_contratos_por_uasg_extruturado['count'] = count

        # Calculando o n˙mero de contratos por uf:
        contratos_por_uf = {}
        uf_contratos = [contrato.uasg.uf() for contrato in contratos]
        contagem_estados = [['State', 'Contratos']]
        for uf in ESTADOS:
            contagem_estados.append([uf,uf_contratos.count(uf)])

        ### Output:
        indicadores = {
                'NOME' : self.nome,
                'CNPJ' : self.cnpj,
                'NUMERO DE PREGOES PARTICIPADOS': n_pregoes_participados,
                'NUMERO DE PREGOES VENCIDOS':contagem_pregoes_vencidos,
                'VALOR MEDIO DOS CONTRATOS':locale.currency(valor_medio_contratos,grouping=True),
                'FREQUENCIA DE CONTRATOS POR ANO':contratos_por_ano,
                'FREQUENCIA DE CONTRATOS POR ESTADO': contagem_estados,
                'FREQUENCIA DE CONTRATOS POR MODALIDADE DE LICITACAO':contratos_por_modalidade,
                'NUMERO MEDIO DE CONTRATOS POR ANO':"%.2f" %media_n_contratos,
                'DURACAO MEDIA DOS CONTRATOS (MES)':"%.2f" %delta_tempo_contratos,
                'FREQUENCIA DE CONTRATOS POR UASG': sorted_contratos_por_uasg_extruturado,
                }
        return indicadores

    def indicadores_rivais(self):
        # Esse mÈtodo retorna um dicion·rio com os principais indicadores sobre
        # participaÁ„o de licitaÁıes e contratos dos rivais de self.
        
        # Acessando informaÁ„o "nome" do dicion·rio resultante "filter_rival":
        dict_rivais = self.filter_rival()
        nomes_rivais = dict_rivais.keys()

        # Contruindo dicion·rio output:
        rivais_indicadores = {}
        for nome in nomes_rivais:
            # Acessando informaÁ„o objeto do dicion·rio resultante
            # "filter_rival":
            objeto_fornecedor_rival = dict_rivais[nome]['obj']

            # Aplicando o mÈtodo "indicadores" em rival:
            indicadores_rival = objeto_fornecedor_rival.indicadores()

            # Adicionando informaÁıes ao output
            rivais_indicadores[nome] = {}
            rivais_indicadores[nome]['ind'] = indicadores_rival
            rivais_indicadores[nome]['obj'] = objeto_fornecedor_rival
        return rivais_indicadores
        
class Declaracao(models.Model):
    id = models.ObjectIdField()
    numero = models.CharField(max_length=10)
    id_uasg = models.ForeignKey(Uasg, on_delete=models.CASCADE)
    id_fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

    def filter_fornecedor_mesmo_pregao(self):
        # Essa funcao retorna uma lista de declaracoes do mesmo pregao ao qual
        # self se refere (aonde "numero" e o codigo do pregao [Ex.:132017] e o
        # id_uasg define o uasg)
        declaracoes_concorrentes = list(Declaracao.objects.filter(numero=self.numero,id_uasg=self.id_uasg_id))
        fornecedores_concorrente = [Fornecedor.objects.get(id=d.id_fornecedor_id) for d in declaracoes_concorrentes]
        return fornecedores_concorrente

    def filter_contrato(self):
        # Essa func„o retorna uma lista de objetos "Contrato" com todos os contratos relacionados ao pregao dessa declaraÁ„o

        contratos_pregao= list(Contrato.objects.filter(numero_aviso_licitacao=self.numero,uasg=self.id_uasg_id))
        return contratos_pregao

class Contrato(models.Model):
    id = models.ObjectIdField()
    identificador = models.CharField(max_length=20)
    uasg = models.ForeignKey(Uasg, on_delete=models.CASCADE)
    modalidade_licitacao = models.IntegerField(blank=True, null=True)
    numero_aviso_licitacao = models.IntegerField(blank=True, null=True)
    codigo_contrato= models.IntegerField(blank=True, null=True)
    licitacao_associada = models.CharField(max_length=20)
    origem_licitacao = models.CharField(max_length=20)
    numero = models.IntegerField(blank=True, null=True)
    objeto = models.CharField(max_length=100)
    numero_processo = models.CharField(max_length=20)
    cnpj_contratada = models.CharField(max_length=20)
    data_assinatura = models.DateField(auto_now=False, auto_now_add=False)
    fundamento_legal = models.CharField(max_length=200)
    data_inicio_vigencia = models.DateField(auto_now=False, auto_now_add=False)
    data_termino_vigencia = models.DateField(auto_now=False, auto_now_add=False)
    valor_inicial = models.IntegerField(blank=True, null=True)

