from djongo import models



UF_LIST = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espirito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MS', 'Mato Grosso do Sul'),
        ('MT', 'Mato Grosso'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB ', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
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
        # Essa funca�ao retorna um dicionario com todos os fornecedores que ja
        # competiram com 'self' em algum pregao.

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

class Contrato(models.Model):
    id = models.ObjectIdField()
    identificador = models.CharField(max_length=20)
    uasg = models.ForeignKey(Uasg, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
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









