from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    instituicao = models.CharField(max_length=100, blank=True)
    profissao = models.CharField(max_length=100, blank=True)
    descricao = models.TextField(max_length=1000, blank=True)
    def __str__(self):
        return self.user.username

class Pergunta(models.Model):
    usuario = models.CharField(max_length=100, default='usuario default')
    titulo = models.CharField(max_length=100, blank=True)
    texto = models.CharField(max_length=1000, default='texto default')
    votos = models.IntegerField(default=0)
    def __str__(self):
        return self.titulo

class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    texto = models.CharField(max_length=1000)
    def __str__(self):
        return self.texto

class VotosPerguntas(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    def __str__(self):
        return self.usuario
