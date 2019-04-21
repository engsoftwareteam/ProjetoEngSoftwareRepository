from django.contrib import admin
from .models import Usuario, Pergunta, Resposta, UserProfileInfo

admin.site.register(Usuario)
admin.site.register(Pergunta)
admin.site.register(Resposta)
admin.site.register(UserProfileInfo)