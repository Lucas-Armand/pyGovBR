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


class Fornecedor(models.Model):
    id = models.ObjectIdField()
    cnpj = models.CharField(max_length=20)
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

class Declaracao(models.Model):
    id = models.ObjectIdField()
    numero = models.CharField(max_length=10)
    id_uasg = models.ForeignKey(Uasg, on_delete=models.CASCADE)
    id_fornecedor = models.ArrayReferenceField(
        to=Fornecedor,
        on_delete=models.CASCADE,
    )









