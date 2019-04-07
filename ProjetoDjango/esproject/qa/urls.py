from django.urls import path

from . import views

app_name = 'qa'
urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('postar_pergunta', views.postar_pergunta, name='postar_pergunta'),
    path('salvar_pergunta', views.salvar_pergunta, name='salvar_pergunta'),
    path('pergunta_postada/<int:pergunta_id>', views.confirmar_pergunta, name='confirmar_pergunta'),
    path('listar_perguntas', views.listar_perguntas, name='listar_perguntas'),
    path('selecionar_pergunta/<int:pergunta_id>', views.selecionar_pergunta, name='selecionar_pergunta'),
    path('deletar_pergunta/<int:pergunta_id>', views.deletar_pergunta, name='deletar_pergunta'),
    path('alterar_pergunta/<int:pergunta_id>', views.alterar_pergunta, name='alterar_pergunta'),
    path('salvar_resposta/<int:pergunta_id>', views.salvar_resposta, name='salvar_resposta'),
    path('resposta_postada/<int:pergunta_id>/<int:resposta_id>', views.confirmar_resposta, name='confirmar_resposta'),
]
