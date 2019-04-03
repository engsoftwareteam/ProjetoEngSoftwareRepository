from django.http import HttpResponse

def home(request):
    return HttpResponse('Ola Mundo')

def clientes(request):
    return HttpResponse('Joao,Maria')