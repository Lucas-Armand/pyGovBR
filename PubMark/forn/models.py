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
    _id = models.ObjectIdField()
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=200)
    uf = models.CharField(max_length=3, choices=UF_LIST)

class Fornecedor(models.Model):
    _id = models.ObjectIdField()
    cnpj = models.CharField(max_length=20)
    nome = models.CharField(max_length=200)
    uf = models.CharField(max_length=3, choices=UF_LIST)
    porte = models.CharField(max_length=20)

class Pregao(models.Model):
    _id = models.ObjectIdField()
    numero = models.CharField(max_length=10)
    uasg = models.ForeignKey(Uasg, on_delete=models.CASCADE)
    fornecedor = models.ArrayReferenceField(
        to=Fornecedor,
        on_delete=models.CASCADE,
    )
    declaracaoIndependente = models.BooleanField
    declaracaoInfantil = models.BooleanField
    declaracaosuperveniente = models.BooleanField








