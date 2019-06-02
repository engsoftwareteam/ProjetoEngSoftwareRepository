from django.test import TestCase, Client
from .models import UserProfileInfo, Pergunta
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
    # def test_deletar_pergunta(self):
    #     pergunta = Pergunta(texto='pergunta')
    #     pergunta.save()
    #     response = self.client.post('deletar_pergunta/pergunta_id'+ str(pergunta.pk))
    #     self.assertContains(response, 'Sua pergunta foi deletada')
