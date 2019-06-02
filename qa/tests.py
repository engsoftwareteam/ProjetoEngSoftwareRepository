from django.test import TestCase, Client
from .models import UserProfileInfo, Pergunta, Resposta
from django.shortcuts import get_object_or_404

# Create your tests here.
class userTest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_registrar_usuario(self):
        req_data = {'username': 'user@test.com','password': 'secret'}
        response = self.client.post('/registrar_usuario', req_data)
        self.assertEquals(response.status_code, 200)
    def test_login_usuario(self):
        req_data = {'username': 'user@test.com','password': 'secret'}
        self.client.post('/registrar_usuario', req_data)
        response = self.client.post('/login_usuario', req_data)
        self.assertRedirects(response, '/menu')
    def test_alterar_senha(self):
        req_data = {'username': 'user@test.com','password': 'secret'}
        self.client.post('/registrar_usuario', req_data)
        req_data = {'username': 'user@test.com','old_password': 'secret', 'new_password': 'secret2', 'confirm_password': 'secret2'}
        response = self.client.post('/alterar_senha', req_data)
        self.assertRedirects(response, '/login_usuario')

class perguntaTest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_postar_pergunta(self):
        req_data = {'username': 'user@test.com','password': 'secret'}
        self.client.post('/registrar_usuario', req_data)
        self.client.post('/login_usuario', req_data)
        req_data={'texto':'pergunta'}
        response = self.client.post('/postar_pergunta', req_data)
        self.assertRedirects(response, '/pergunta_postada/1')
    def test_deletar_pergunta(self):
        pergunta = Pergunta(texto='pergunta')
        pergunta.save()
        response = self.client.post('/deletar_pergunta/1')
        self.assertContains(response, 'Sua pergunta foi deletada')
    def test_listar_perguntas(self):
        pergunta = Pergunta(texto='pergunta')
        pergunta.save()
        pergunta2 = Pergunta(texto='pergunta2')
        pergunta2.save()
        response = self.client.post('/listar_perguntas')
        self.assertContains(response, 'pergunta')
        self.assertContains(response, 'pergunta2')

class resposta_test(TestCase):
    def setUp(self):
        self.client = Client()
    def test_postar_resposta(self):
        req_data = {'username': 'user@test.com','password': 'secret'}
        self.client.post('/registrar_usuario', req_data)
        self.client.post('/login_usuario', req_data)
        pergunta = Pergunta(texto='pergunta')
        pergunta.save()   
        req_data = {'texto': 'resposta'}
        response = self.client.post('/postar_resposta/1', req_data)
        self.assertRedirects(response, '/resposta_postada/1/1')
    def test_alterar_resposta(self):
        pergunta = Pergunta(texto='pergunta')
        pergunta.save()   
        resposta = Resposta(texto='resposta', pergunta_id=1)
        resposta.save()
        req_data = {'texto_alterado': 'resposta_alterada'}
        response = self.client.post('/alterar_resposta/1', req_data)
        self.assertEquals(response.status_code, 200)
