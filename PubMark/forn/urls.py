from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /forn/00097117000135
    path('<str:CNPJ>/', views.detail, name='detail'),
    path('<str:CNPJ>/indicadores', views.indicadores, name='indicadores'),
    path('<str:CNPJ>/rivais', views.rivais, name='rivais'),

]
