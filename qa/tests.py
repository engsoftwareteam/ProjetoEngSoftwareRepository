from django.test import TestCase, Client
from .models import Profile, Pergunta, Resposta, VotosPerguntas
from django.shortcuts import get_object_or_404

# Create your tests here.
class userTest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_registrar_usuario(self):
        req_data = {'username': 'user@test.com','password': 'secret', 'email': 'useremail@test.com', 'password_confirm':'secret'}
        response = self.client.post('/registrar_usuario', req_data)
        self.assertEquals(response.status_code, 302)
    def test_login_usuario(self):
        req_data = {'username': 'user@test.com','password': 'secret', 'email': 'useremail@test.com'}
        self.client.post('/registrar_usuario', req_data)
        req_data = {'username': 'user@test.com','password': 'secret'}
        response = self.client.post('/login_usuario', req_data)
        self.assertEquals(response.status_code, 302)
    def test_meu_perfil(self):
        req_data = {'username': 'user@test.com','password': 'secret', 'email': 'useremail@test.com'}
        self.client.post('/registrar_usuario', req_data)
        req_data = {'username': 'user@test.com','password': 'secret'}
        response = self.client.post('/login_usuario', req_data)
        req_data = {'username': 'user@test.com', 'new_password': 'secret2', 'email': 'useremail@test.com', 'new_password2':'secret2', 'instituicao':'faculdade', 'profissao':'estudante', 'descricao':'oi'}
        response = self.client.post('/meu_perfil', req_data)
        self.assertEquals(response.status_code, 302)
    def test_meus_posts(self):
        req_data = {'username': 'user@test.com','password': 'secret', 'email': 'useremail@test.com'}
        self.client.post('/registrar_usuario', req_data)
        req_data = {'username': 'user@test.com','password': 'secret'}
        self.client.post('/login_usuario', req_data)
        pergunta = Pergunta(texto='pergunta')
        pergunta.save()  
        resposta = Resposta(texto='resposta', pergunta_id=1)
        resposta.save()
        response = self.client.post('/meus_posts')
        self.assertEquals(response.status_code, 200)
    def test_remover_usuario(self):
        req_data = {'username': 'user@test.com','password': 'secret', 'email': 'useremail@test.com'}
        self.client.post('/registrar_usuario', req_data)
        req_data = {'username': 'user@test.com','password': 'secret'}
        self.client.post('/login_usuario', req_data)
        response = self.client.post('/remover_usuario', req_data)
        self.assertEquals(response.status_code, 302)

class perguntaTest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_postar_pergunta(self):
        req_data = {'username': 'user@test.com','password': 'secret', 'email': 'useremail@test.com'}
        self.client.post('/registrar_usuario', req_data)
        req_data = {'username': 'user@test.com','password': 'secret'}
        self.client.post('/login_usuario', req_data)
        req_data={'texto':'pergunta', 'titulo':'new', 'tags':'tag1,tag2','votos':0}
        response = self.client.post('/postar_pergunta', req_data)
        self.assertEquals(response.status_code,200)
    def test_deletar_pergunta(self):
        pergunta = Pergunta(texto='pergunta')
        pergunta.save()
        response = self.client.post('/deletar_pergunta/1')
        self.assertEquals(response.status_code, 200)
    def test_listar_perguntas(self):
        pergunta = Pergunta(texto='pergunta',titulo='new')
        pergunta.save()
        pergunta2 = Pergunta(texto='pergunta2', titulo='new')
        pergunta2.save()
        response = self.client.post('/listar_perguntas')
        self.assertEquals(response.status_code, 200)
    def test_alterar_pergunta(self):
        pergunta = Pergunta(texto='pergunta', tags='tag1,tag2',votos=0)
        pergunta.save()
        req_data = {'texto_alterado': 'pergunta_alterada', 'tags_alterado':'tag3,tag4', 'titulo_alterado':'hello'}
        response = self.client.post('/alterar_pergunta/1', req_data)
        self.assertEquals(response.status_code, 302)    	


class resposta_test(TestCase):
    def setUp(self):
        self.client = Client()
    def test_postar_resposta(self):
        req_data = {'username': 'user@test.com','password': 'secret', 'email': 'useremail@test.com'}
        self.client.post('/registrar_usuario', req_data)
        req_data = {'username': 'user@test.com','password': 'secret'}
        self.client.post('/login_usuario', req_data)
        pergunta = Pergunta(texto='pergunta', titulo='new')
        pergunta.save()   
        req_data = {'texto': 'resposta'}
        response = self.client.post('/postar_resposta/1', req_data)
        self.assertEquals(response.status_code, 302)
    def test_alterar_resposta(self):
        pergunta = Pergunta(texto='pergunta')
        pergunta.save()   
        resposta = Resposta(texto='resposta', pergunta_id=1)
        resposta.save()
        req_data = {'texto_alterado': 'resposta_alterada'}
        response = self.client.post('/alterar_resposta/1', req_data)
        self.assertEquals(response.status_code, 302)
    def test_deletar_resposta(self):
        pergunta = Pergunta(texto='pergunta')
        pergunta.save()  
        vote = VotosPerguntas(usuario= 'user1', pergunta=pergunta)
        vote.save()
        resposta = Resposta(texto='resposta', pergunta_id=1)
        resposta.save()
        response = self.client.post('/deletar_resposta/1')
        self.assertContains(response, 'Página Inicial')
        
class vote_pergunta_test(TestCase):
    def setUp(self):
        self.client = Client()
    def test_vote_perguta(self):
        req_data = {'username': 'user1@test.com','password': 'secret', 'email': 'useremail@test.com'}
        self.client.post('/registrar_usuario', req_data)
        req_data = {'username': 'user1@test.com','password': 'secret'}
        self.client.post('/login_usuario', req_data)
        pergunta = Pergunta(texto='pergunta', tags='tag1,tag2',votos=0)
        pergunta.save()   
        req_data={'votos':'1'}
        response = self.client.post('/VotePergunta/1', req_data)
        self.assertEquals(response.status_code, 302)
    def test_vote_resposta(self):
        req_data = {'username': 'user1@test.com','password': 'secret', 'email': 'useremail@test.com'}
        self.client.post('/registrar_usuario', req_data)
        req_data = {'username': 'user1@test.com','password': 'secret'}
        self.client.post('/login_usuario', req_data)
        pergunta = Pergunta(texto='pergunta', tags='tag1,tag2',votos=0)
        pergunta.save()   
        resposta = Resposta(texto='resposta', pergunta_id=1, votos=0)
        resposta.save()
        req_data={'votosResposta1':'1'}
        response = self.client.post('/VoteResposta/1/1', req_data)
        self.assertEquals(response.status_code, 302)
				
