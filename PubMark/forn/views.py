from django.http import HttpResponse

from .models import Fornecedor
import pandas as pd


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request,CNPJ):
    fornecedor = Fornecedor.objects.get(cnpj = CNPJ)
    atributos_fornecedor = vars(fornecedor)
    return HttpResponse(str(atributos_fornecedor))

def indicadores(request,CNPJ):
    fornecedor = Fornecedor.objects.get(cnpj = CNPJ)
    indicadores = fornecedor.indicadores()
    return HttpResponse(str(indicadores))

def rivais(request,CNPJ):
    fornecedor = Fornecedor.objects.get(cnpj = CNPJ)
    rivais = fornecedor.indicadores_rivais()
    return HttpResponse(str(rivais))




