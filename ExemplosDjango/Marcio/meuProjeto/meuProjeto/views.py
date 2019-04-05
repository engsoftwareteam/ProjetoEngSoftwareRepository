from django.http import HttpResponse

def home(request):
    return HttpResponse('Ola Mundo')

def clientes(request):
    return HttpResponse('Joao,Maria')

def cliente_detalhe(request):
    return HttpResponse('ola')

def cliente_por_nome(request,nome):
    return HttpResponse(nome)