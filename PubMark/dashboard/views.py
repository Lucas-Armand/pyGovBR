from django.shortcuts import render
from django.http import HttpResponse
from django.template import  loader
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import re
''''
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

'''

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
            return redirect("detail",CNPJ = cnpj)
        
    # Lidando com acesso "inicial", que deve selecionar um CNPJ:
    template = loader.get_template('dashboard\\\\form.html')
    context = {}
    return HttpResponse(template.render(context, request))


