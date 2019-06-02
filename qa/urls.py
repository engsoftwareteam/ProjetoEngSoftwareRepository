from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'qa'
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('meu_perfil', views.meu_perfil, name='meu_perfil'),
    path('postar_pergunta', views.postar_pergunta, name='postar_pergunta'),
    path('listar_perguntas', views.listar_perguntas, name='listar_perguntas'),
    path('selecionar_pergunta/<int:pergunta_id>', views.selecionar_pergunta, name='selecionar_pergunta'),
    path('deletar_pergunta/<int:pergunta_id>', views.deletar_pergunta, name='deletar_pergunta'),
    path('alterar_pergunta/<int:pergunta_id>', views.alterar_pergunta, name='alterar_pergunta'),
    path('postar_resposta/<int:pergunta_id>', views.postar_resposta, name='postar_resposta'),
    path('selecionar_resposta/<int:resposta_id>', views.selecionar_resposta, name='selecionar_resposta'),
    path('alterar_resposta/<int:resposta_id>', views.alterar_resposta, name='alterar_resposta'),
    path('upVotePergunta/<int:pergunta_id>', views.upVotePergunta, name='upVotePergunta'),
    path('deletar_resposta/<int:resposta_id>', views.deletar_resposta, name='deletar_resposta'),
    path('cadastrar_usuario', TemplateView.as_view(template_name='qa/cadastrar_usuario.html'), name='cadastrar_usuario'),

    path('registrar_usuario', views.registrar_usuario, name='registrar_usuario'),
    path('login_usuario', views.login_usuario, name='login_usuario'),
    path('logout_usuario', views.logout_usuario, name='logout_usuario'),
    path('logged', views.logged, name='logged'),
    path('meus_posts', views.meus_posts, name='meus_posts'),
    path('remover_usuario', views.remover_usuario, name='remover_usuario')
]
