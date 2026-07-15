from django.urls import path

from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.lista_projetos, name='lista'),
    path('cases/', views.cases, name='cases'),
    path('<slug:slug>/', views.detalhe_projeto, name='detalhe'),
]
