from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Pergunta

def index(request):
    return HttpResponse("Ola, voce esta no index do app Q&A")

def fazer_pergunta(request):
    return render(request, 'qa/fazer_pergunta.html')

def salvar_pergunta(request):
    try:
        pergunta = Pergunta(usuario=request.POST['usuario'], texto=request.POST['texto'])
        pergunta.save()
    except (KeyError, pergunta.pk == None):
        return HttpResponse("Pergunta nao foi salva")
    return HttpResponseRedirect('/qa/pergunta_salva/%s' %pergunta.id)

def confirmar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    context = {'pergunta': pergunta}    
    return render(request, 'qa/confirmacao_pergunta.html', context)

def menu(request):
    return render(request, 'qa/menu.html')

def listar_perguntas(request):
    perguntas = Pergunta.objects.all()
    context = {'perguntas': perguntas}
    return render(request, 'qa/lista_perguntas.html', context)

def selecionar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    context = {'pergunta': pergunta}    
    return render(request, 'qa/pergunta_selecionada.html', context)