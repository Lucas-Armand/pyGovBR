import pprint
from forn.models import Contrato,Declaracao,Fornecedor,Uasg

### Testes unitário: 
# Tentando o acesso aos objetos
contrato = Contrato.objects.get(pk=1)
declaracao = Declaracao.objects.get(pk=1)
fornecedor = Fornecedor.objects.get(pk=1)
usag = Uasg.objects.get(pk=10001)

## Usando as Funções do contrato
# Testando os métodos de Declaração
declaracao.filter_fornecedor_mesmo_pregao()
declaracao.filter_contrato()

# Testando os métodos de Fornecedor
fornecedor.filter_contrato()
fornecedor.filter_rival()
fornecedor.filter_declaracao()
fornecedor.indicadores()
fornecedor.indicadores_rivais()

## Testando nova aplicação:

### Teste Ponta-a-Ponta
opemacs = Fornecedor.objects.get(id=925)
print('indicadores Opemacs')
print(opemacs.indicadores())
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(opemacs.indicadores())
print('')
print('indicadores concorrentes Opemacs')
pp.pprint(opemacs.indicadores_rivais())

