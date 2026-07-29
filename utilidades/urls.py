from django.urls import path

from . import views

app_name = 'utilidades'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('gerador-de-senha/', views.gerador_senha, name='gerador_senha'),
    path('validador-cpf-cnpj/', views.validador_documento, name='validador_documento'),
    path('formatador-json/', views.formatador_json, name='formatador_json'),
    path('conversor-base64/', views.conversor_base64, name='conversor_base64'),
    path('gerador-hash/', views.gerador_hash, name='gerador_hash'),
    path('gerador-uuid/', views.gerador_uuid, name='gerador_uuid'),
    path('contador-texto/', views.contador_texto, name='contador_texto'),
    path('conversor-timestamp/', views.conversor_timestamp, name='conversor_timestamp'),
    path('minificador-codigo/', views.minificador_codigo, name='minificador_codigo'),
    path('calculadora-tokens/', views.calculadora_tokens, name='calculadora_tokens'),
    path('gerador-prompts/', views.gerador_prompts, name='gerador_prompts'),
    path('json-para-markdown/', views.json_para_markdown, name='json_para_markdown'),
    path('extrator-codigo-ia/', views.extrator_codigo_ia, name='extrator_codigo_ia'),
    path('gerador-readme/', views.gerador_readme, name='gerador_readme'),
    path('seguranca-owasp/', views.seguranca_owasp, name='seguranca_owasp'),
    path('agente-orientador/', views.agente_orientador, name='agente_orientador'),
    path('seo-especialista/', views.seo_especialista, name='seo_especialista'),
    path('achador-oportunidades/', views.achador_oportunidades, name='achador_oportunidades'),
    path('mini-curso/', views.mini_curso, name='mini_curso'),
]








