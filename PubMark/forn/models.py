from djongo import models



UF_LIST = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'AmapÃ¡'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'CearÃ¡'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espirito Santo'),
        ('GO', 'GoiÃ¡s'),
        ('MA', 'MaranhÃ£o'),
        ('MS', 'Mato Grosso do Sul'),
        ('MT', 'Mato Grosso'),
        ('MG', 'Minas Gerais'),
        ('PA', 'ParÃ¡'),
        ('PB ', 'ParaÃ­ba'),
        ('PR', 'ParanÃ¡'),
        ('PE', 'Pernambuco'),
        ('PI', 'PiauÃ­'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'RondÃ´nia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'SÃ£o Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
        )


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
    uf = models.CharField(max_length=3, choices=UF_LIST)

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
        # Essa funcão retorna um dicionario com todos os fornecedores que ja
        # competiram com 'self' em algum pregao. O dicionário é estruturado
        # por:
            # count -> Número de vezes que a empresa concorreu com "self"
            # obj -> Que é o objeto fornecedor relacionado á empresa

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
        # Essa funcão retorna uma lista de objetos "Contrato" com todos os
        # contratos relacionado ao cnpj de "self"

        cnpj = self.cnpj
        contratos = list(Contrato.objects.filter(cnpj_contratada = cnpj))
        return contratos

    def indicadores(self):
        # Esse método retorna um dicionário com os principais indicadores sobre
        # participação de licitações e contratos de self.

        # Acessando dados:
        declaracoes = self.filter_declaracao()
        contratos = self.filter_contrato()

        ### Processando dados
        
        # Contagem do número de pregões participados:
        n_pregoes_participados = len(declaracoes)
        
        # Calculando numero de pregoes vencidos:
        codigo_pregoes_participados = [declaracao.numero for declaracao in declaracoes]
        contagem_pregoes_vencidos = 0
        for contrato in contratos:
            if contrato.numero_aviso_licitacao in codigo_pregoes_participados:
                contagem_pregoes_vencidos += 1

        # Calculo do valor médio dos contratos:
        valores_dos_contratos = [contrato.valor_inicial if contrato.valor_inicial!= None else 0 for contrato in contratos]
        if len(contratos)>0:
            valor_medio_contratos = sum(valores_dos_contratos)/len(contratos)
        else:
            valor_medio_contratos = 0

        # Calculando a frequencia de contratos por ano:
        contratos_por_ano = {}
        ano_contratos = [contrato.data_assinatura.year for contrato in contratos]
        anos = set(ano_contratos)
        for ano in anos:
            contratos_por_ano[ano] = ano_contratos.count(ano)
        
        # Calculando a frequencia das modalidades de licitação dos contratos:
        contratos_por_modalidade = {}
        modalidade_contratos = [contrato.modalidade_licitacao for contrato in contratos]
        modalidades = set(modalidade_contratos)
        for modalidade in modalidades:
            contratos_por_modalidade[modalidade] = modalidade_contratos.count(modalidade)

        # Calculando a frequencia de contratos por uasg:
        contratos_por_uasg = {}
        uasg_conratos = [contrato.uasg.nome for contrato in contratos]
        uasgs = set(uasg_contratos)
        for uasg in uasgs:
            contratos_por_uasg[uasg.nome] = uasg_conratos.count(uasg.nome)
        sorted_contratos_por_uasg = sorted(contratos_por_uasg.items(), key=lambda kv: kv[1], reverse=True)




        ### Output:
        indicadores = {
                'NUMERO DE PREGOES PARTICIPADOS': n_pregoes_participados,
                'NUMERO DE PREGOES VENCIDOS':contagem_pregoes_vencidos,
                'VALOR MEDIO DE CONTRATOS':valor_medio_contratos,
                'FREQUENCIA DE CONTRATOS POR ANO':contratos_por_ano,
                'FREQUENCIA DE CONTRATOS POR MODALIDADE DE LICITACAO':contratos_por_modalidade,
                'FREQUENCIA DE CONTRATOS POR UASG': sorted_contratos_por_uasg,
                }
        return indicadores

    def indicadores_rivais(self):
        # Esse método retorna um dicionário com os principais indicadores sobre
        # participação de licitações e contratos dos rivais de self.
        
        # Acessando informação "nome" do dicionário resultante "filter_rival":
        dict_rivais = self.filter_rival()
        nomes_rivais = dict_rivais.keys()

        # Contruindo dicionário output:
        rivais_indicadores = {}
        for nome in nomes_rivais:
            # Acessando informação objeto do dicionário resultante
            # "filter_rival":
            objeto_fornecedor_rival = dict_rivais[nome]['obj']

            # Aplicando o método "indicadores" em rival:
            indicadores_rival = objeto_fornecedor_rival.indicadores()

            # Adicionando informações ao output
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
        # Essa funcão retorna uma lista de objetos "Contrato" com todos os contratos relacionados ao pregao dessa declaração

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

