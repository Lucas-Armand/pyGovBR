from .models import Uasg, Fornecedor, Pregao
from pymongo import MongoClient

client = MongoClient('localhost', 27017)


def findOneUasgByCodigo(codigo):
    db = client['caranda']
    col = db['forn_uasg']

    result = col.find_one({"codigo": codigo})


    return result


def findUasgByUf(uf):
    db = client['caranda']
    col = db['forn_uasg']

    result = col.find({"uf": uf})

    return result


def findUasgByNome(nome):
    db = client['caranda']
    col = db['forn_uasg']

    result = col.find({"nome": nome})

    return result


def findOneForncedorByCnpj(cnpj):
    db = client['caranda']
    col = db['forn_fornecedor']

    result = col.find_one({"cnpj": cnpj})

    return result


def findFornecedorByUf(uf):
    db = client['caranda']
    col = db['forn_fornecedor']

    result = col.find({"uf": uf})

    return result


def findFornecedorByNome(nome):
    db = client['caranda']
    col = db['forn_fornecedor']

    result = col.find({"nome": nome})

    return result


