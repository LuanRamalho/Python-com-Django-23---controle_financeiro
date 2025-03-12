from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adicionar/receita/', views.adicionar_receita, name='adicionar_receita'),
    path('adicionar/despesa/', views.adicionar_despesa, name='adicionar_despesa'),
    path('editar/receita/<int:receita_id>/', views.editar_receita, name='editar_receita'),
    path('excluir/receita/<int:receita_id>/', views.excluir_receita, name='excluir_receita'),
    path('editar/despesa/<int:despesa_id>/', views.editar_despesa, name='editar_despesa'),
    path('excluir/despesa/<int:despesa_id>/', views.excluir_despesa, name='excluir_despesa'),
    path('gerar_grafico/', views.gerar_grafico, name='gerar_grafico'),
    path('pdf/', views.gerar_pdf, name='gerar_pdf'),
]
