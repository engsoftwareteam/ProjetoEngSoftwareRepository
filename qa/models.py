from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    campo = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.user.username

class Usuario(models.Model):
    usuario = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=25)
    def __str__(self):
        return self.usuario

class Pergunta(models.Model):
    usuario = models.CharField(max_length=100, default='usuario default')
    texto = models.CharField(max_length=1000, default='texto default')
    def __str__(self):
        return self.texto

class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    texto = models.CharField(max_length=1000)
    def __str__(self):
        return self.texto
