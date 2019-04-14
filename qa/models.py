from django.db import models

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
