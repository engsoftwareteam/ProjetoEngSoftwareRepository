from django.test import TestCase, Client
from .models import UserProfileInfo

# Create your tests here.
class userTest(TestCase):
    def test_registrar_usuario(self):
        req_data = {'username': 'user@test.com','password': 'secret'}
        response = self.client.post('/registrar_usuario', req_data)
        self.assertEquals(response.status_code, 200)