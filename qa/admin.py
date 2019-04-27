from django.contrib import admin
from .models import Pergunta, Resposta, Profile

admin.site.register(Pergunta)
admin.site.register(Resposta)
admin.site.register(Profile)