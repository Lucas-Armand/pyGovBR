from _ast import mod

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

MODALIDADE_LICITACAO_LIST = (
    (1, 'CONVITE'),
    (2, 'TOMADA DE PRECOS'),
    (3, 'CONCORRENCIA'),
    (4, 'CONCORRENCIA INTERNACIONAL'),
    (5, 'PREGAO'),
    (6, 'DISPENSA DE LICITACAO'),
    (7, 'INEXIGIBILIDADE DE LICITACAO'),
)

TIPO_DE_CONTRATO_LIST = (
    (50, 'CONTRATO'),
    (51, 'CREDENCIAMENTO'),
    (52, 'COMODATO'),
    (53, 'ARRENDAMENTO'),
    (54, 'CONCESSAO'),
    (55, 'TERMO ADITIVO'),
    (56, 'TERMO DE ADESAO'),
    (57, 'CONVENIO'),
    (60, 'TERMO DE APOSTILAMENTO'),
)

NATUREZA_JURIDICA_LIST = (

)

PORTE_EMPRESA_LIST = (

)

RAMO_NEGOCIO_LIST = (

)

class Municipio(models.Model):

    # atomic Fields
    # embeedded Fields one-to-one
    # choices Fields

    class Meta:
        abstract = True
    abstract = True



class Orgao(models.Model):

    # atomic Fields
    # embeedded Fields one-to-one
    # choices Fields

    class Meta:
        abstract = True


class Cnae(models.Model):

    # atomic Fields
    # embeedded Fields one-to-one
    # choices Fields

    class Meta:
        abstract = True

class UnidadeCadastradora(models.Model):

    # atomic Fields
    # embeedded Fields one-to-one
    # choices Fields

    class Meta:
        abstract = True


class Uasg(models.Model):

    _id = models.ObjectIdField()

    # atomic Fields
    nome = models.CharField(max_length=200)
    cep = models.CharField(max_length=20)
    total_fornecedores_cadastrados = models.IntegerField(blank=True, null=True)
    total_fornecedores_cadastrados = models.IntegerField(blank=True, null=True)
    unidade_cadastradora = models.BooleanField(default=False)
    ativo = models.BooleanField(default=False)

    # embeedded Fields one-to-one
    orgao = models.EmbeddedModelField(model_container=Orgao)  # Atributo origem id_orgao
    municipio = models.EmbeddedModelField(model_container=Municipio)  # Atributo origem id_municipio

    class Meta:
        abstract = True


class Fornecedor(models.Model):

    _id = models.ObjectIdField()

    # atomic Fields
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=20, blank=True, null=True)
    nome = models.CharField(max_length=200, blank=True, null=True)
    ativo = models.BooleanField(default=False)
    recadastrado = models.BooleanField(default=False)
    habilitado_licitar = models.BooleanField(default=False)

    # embeedded Fields one-to-one
    municipio = models.EmbeddedModelField(model_container=Municipio)  # Atributo origem id_municipio
    cnae = models.EmbeddedModelField(model_container=Cnae)  # Atributo origem id_cnae
    unidade_cadastradora = models.EmbeddedModelField(model_container=UnidadeCadastradora)  # Atributo origem id_unidade_cadastradora

    # choices Fields
    uf = models.CharField(max_length=3, choices=UF_LIST)
    natureza_juridica = models.IntegerField(choices=NATUREZA_JURIDICA_LIST)
    porte_empresa = models.CharField( choices=PORTE_EMPRESA_LIST)
    ramo_negocio = models.CharField(max_length=4, choices=RAMO_NEGOCIO_LIST)

    class Meta:
        abstract = True

class Pregao(models.Model):

    # atomic Fields
    codigo_portaria
    data_portaria
    codigo_processo
    tipo_pregao
    tipo_compra
    objeto_pregao
    data_abertura_edital
    data_inicio_proposta
    data_fim_proposta


    # embeedded Fields one-to-one
    uasg
    orgao

    # list Fields one-to-many
    resultados
    declaracoes
    termos
    itens

    class Meta:
        abstract = True

class Licitacao(models.Model):

    # atomic Fields
    numero_aviso_licitacao
    identificador_licitacao
    tipo_pregao
    situacao_aviso
    objeto
    numero_processo
    tipo_recurso
    endereco_entrega
    numero_itens_licitacao
    nome_responsavel
    funcao_responsavel
    data_entrega_edital
    endereco_entrega_edital
    data_abertura_proposta
    data_entrega_proposta
    data_publicacao




    # embeedded Fields one-to-one
    uasg = models.EmbeddedModelField(model_container=Uasg)
    pregao = models.EmbeddedModelField(model_container=Pregao)

    # list Fields one-to-many
    itens = models.ListField()

    # choices Fields
    modalidade_licitacao = models.CharField(blank=True, null=True, choices=MODALIDADE_LICITACAO_LIST)

    class Meta:
        abstract = True


class Contrato(models.Model):

    _id = models.ObjectIdField()

    # atomic Fields
    identificador = models.CharField(max_length=20, blank=True, null=True)
    numero_aviso_licitacao = models.IntegerField(blank=True, null=True)
    origem_licitacao = models.CharField(max_length=20, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    objeto = models.CharField(max_length=100, blank=True, null=True )
    numero_processo = models.CharField(max_length=20, blank=True, null=True)
    data_assinatura = models.DateField(auto_now=False, auto_now_add=False)
    fundamento_legal = models.CharField(max_length=200, blank=True, null=True)
    data_inicio_vigencia = models.DateField(auto_now=False, auto_now_add=False)
    data_termino_vigencia = models.DateField(auto_now=False, auto_now_add=False)
    valor_inicial = models.IntegerField(blank=True, null=True)

    # embeedded Fields one-to-one
    uasg = models.EmbeddedModelField(model_container=Uasg)
    fornecedor = models.EmbeddedModelField(model_container=Fornecedor)  # originado do  atributo cnpj_contratada
    licitacao = models.CharField(odel_container=Licitacao)  # Atributo origem licitacao_associada

    # list Fields one-to-many
    aditivos = models.ListField()  # Atributo origem aditivos_do_contrato (model_container=AditivoContrato)
    apostilamentos = models.ListField()  # Atributo origem apostilamentos_do_contrato (model_container=ApostilamentoContrato)
    eventos = models.ListField()  # Atributo origem eventos_do_contrato (model_container=EventoContrato)


    # choices Fields
    modalidade_licitacao = models.IntegerField(blank=True, null=True, choices=MODALIDADE_LICITACAO_LIST)
    codigo_contrato = models.IntegerField(blank=True, null=True, choices=CODIGO_CONTRATO_LIST)