from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('', views.lista_cursos, name='lista'),
    path('<slug:slug>/', views.trilha_curso, name='trilha'),
    path('licao/<int:licao_id>/', views.executar_licao, name='licao'),
]
