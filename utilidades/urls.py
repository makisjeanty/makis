from django.urls import path

from . import views

app_name = 'utilidades'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('gerador-de-senha/', views.gerador_senha, name='gerador_senha'),
    path('validador-cpf-cnpj/', views.validador_documento, name='validador_documento'),
    path('formatador-json/', views.formatador_json, name='formatador_json'),
    path('conversor-base64/', views.conversor_base64, name='conversor_base64'),
]
