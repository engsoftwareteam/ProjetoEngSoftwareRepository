from django.contrib import admin
from .models import Pergunta, Resposta, Profile, VotosPerguntas

admin.site.register(Pergunta)
admin.site.register(Resposta)
admin.site.register(VotosPerguntas)
admin.site.register(Profile)