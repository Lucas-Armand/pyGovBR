from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.template import  loader
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from forn.models import Fornecedor
import json
import re

def index(request):
    # Lidando com segundo acesso, uma vez que já se tem CNPJ:
    if request.method == "POST":
        # Recebendo post (QueryDict):
        form = request.POST 

        # Transformando objeto em dicioniario
        form = dict(form)

        # Se a entrade cnpj foi correta
        if 'cnpj' in form.keys():
            cnpj_punctification = str(form['cnpj'][0])
            cnpj = re.sub('\.|/|-','',cnpj_punctification)
            fornecedor = Fornecedor.objects.get(cnpj = cnpj)
            ind = fornecedor.indicadores()
            #ind['NUMERO MEDIO DE CONTRATO POR ANO'] = ''
            #ind['DURACAO MEDIA DOS CONTRATOS (MES)'] = ''
            # return redirect("/dash")
            # return redirect("detail",CNPJ = cnpj)

            return render_to_response('board/dashboard.html',                   
                                       {"nome_empresa":ind['NOME'],
                                        "cnpj" : ind['CNPJ'],           
                                        "nome_1": 'VALOR ANUAL MÉDIO DOS CONTRATOS',
                                        "valor_contrato_ano":  ind['VALOR MEDIO DOS CONTRATOS'],  
                                        "nome_2": "QUANTIDADE DE CONTRATOS POR ANO",
                                        "n_contrato_ano": ind['NUMERO MEDIO DE CONTRATOS POR ANO'],                  
                                        "freq_contratos_uasg":json.dumps(ind['FREQUENCIA DE CONTRATOS POR UASG']),
                                        "nome_3": "DURAÇÃO MÉDIA DOS CONTRATOS (MESES)",
                                        "duracao_contratos_mes": ind['DURACAO MEDIA DOS CONTRATOS (MES)']})  
        
    # Lidando com acesso "inicial", que deve selecionar um CNPJ:
    template = loader.get_template('board/form.html')
    context = {}
    return HttpResponse(template.render(context, request))

