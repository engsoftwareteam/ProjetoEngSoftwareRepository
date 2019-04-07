from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Pergunta

def index(request):
    return HttpResponse("Ola, voce esta no index do app Q&A")

# renderiza html com menu contendo as funcionalidades existentes
def menu(request):
    return render(request, 'qa/menu.html')

# renderiza html com o formulario para fazer novas perguntas
def fazer_pergunta(request):
    return render(request, 'qa/fazer_pergunta.html')

# responsavel por salvar a pergunta no banco de dados
def salvar_pergunta(request):
    try:
        pergunta = Pergunta(usuario=request.POST['usuario'], texto=request.POST['texto'])
        pergunta.save()
    except (KeyError, pergunta.pk == None):
        return HttpResponse("Pergunta nao foi salva")
    return HttpResponseRedirect('/qa/pergunta_salva/%s' %pergunta.id)

# renderiza html com confirmacao que a pergunta foi salva
def confirmar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    context = {'pergunta': pergunta}    
    return render(request, 'qa/confirmacao_pergunta_salva.html', context)

# renderiza html com a lista de perguntas ja feitas
def listar_perguntas(request):
    perguntas = Pergunta.objects.all()
    context = {'perguntas': perguntas}
    return render(request, 'qa/lista_perguntas.html', context)

# busca pergunta selecionada no BD e renderiza o html com informacoes dela
def selecionar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    context = {'pergunta': pergunta}    
    return render(request, 'qa/pergunta_selecionada.html', context)

# responsavel por deletar a pergunta selecionada do BD
def deletar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    try:
        pergunta.delete()
    except (KeyError, pergunta.pk != None):
        return HttpResponse("Pergunta nao foi deletada")
    return render(request, 'qa/confirmacao_pergunta_deletada.html')

# responsavel por alterar o texto da pergunta selecionada no BD
def alterar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    pergunta.texto = request.POST['texto_alterado']
    pergunta.save()
    context = {'pergunta': pergunta}    
    return render(request, 'qa/confirmacao_pergunta_alterada.html', context)