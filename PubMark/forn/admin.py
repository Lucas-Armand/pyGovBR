from django.contrib import admin
from .models import Uasg, Fornecedor, Declaracao

admin.site.register([Uasg, Fornecedor, Declaracao])
