from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'qa'
urlpatterns = [
    path('', TemplateView.as_view(template_name='qa/menu.html'), name='menu'),
    path('menu', TemplateView.as_view(template_name='qa/menu.html'), name='menu'),
    path('postar_pergunta', views.postar_pergunta, name='postar_pergunta'),
    path('pergunta_postada/<int:pergunta_id>', views.confirmar_pergunta, name='confirmar_pergunta'),
    path('listar_perguntas', views.listar_perguntas, name='listar_perguntas'),
    path('selecionar_pergunta/<int:pergunta_id>', views.selecionar_pergunta, name='selecionar_pergunta'),
    path('deletar_pergunta/<int:pergunta_id>', views.deletar_pergunta, name='deletar_pergunta'),
    path('alterar_pergunta/<int:pergunta_id>', views.alterar_pergunta, name='alterar_pergunta'),
    path('postar_resposta/<int:pergunta_id>', views.postar_resposta, name='postar_resposta'),
    path('resposta_postada/<int:pergunta_id>/<int:resposta_id>', views.confirmar_resposta, name='confirmar_resposta'),
    path('selecionar_resposta/<int:resposta_id>', views.selecionar_resposta, name='selecionar_resposta'),
    path('alterar_resposta/<int:resposta_id>', views.alterar_resposta, name='alterar_resposta'),
    path('deletar_resposta/<int:resposta_id>', views.deletar_resposta, name='deletar_resposta'),
    path('cadastrar_usuario', TemplateView.as_view(template_name='qa/cadastrar_usuario.html'), name='cadastrar_usuario'),
    path('salvar_usuario', views.salvar_usuario, name='salvar_usuario'),

    path('home', TemplateView.as_view(template_name='qa/home.html'), name='home'),

    path('registrar_usuario', views.registrar_usuario, name='registrar_usuario'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('special', views.special, name='special'),
]
