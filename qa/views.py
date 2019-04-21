from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Usuario, Pergunta, Resposta

def index(request):
    return HttpResponse("Ola, voce esta no index do app Q&A")

# renderiza html com menu contendo as funcionalidades existentes
def menu(request):
    return render(request, 'qa/menu.html')

# renderiza html com o formulario para fazer novas perguntas
def postar_pergunta(request):
    return render(request, 'qa/postar_pergunta.html')

# responsavel por salvar a pergunta no BD
def salvar_pergunta(request):
    try:
        pergunta = Pergunta(usuario=request.POST['usuario'], texto=request.POST['texto'])
        pergunta.save()
    except (KeyError, pergunta.pk == None):
        return HttpResponse("Pergunta nao foi salva")
    return HttpResponseRedirect('/pergunta_postada/%s' %pergunta.id)

# renderiza html com confirmacao que a pergunta foi salva
def confirmar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    context = {'pergunta': pergunta}    
    return render(request, 'qa/confirmacao_pergunta_postada.html', context)

# renderiza html com a lista de perguntas ja feitas
def listar_perguntas(request):
    perguntas = Pergunta.objects.all()
    context = {'perguntas': perguntas}
    return render(request, 'qa/lista_perguntas.html', context)

# busca pergunta selecionada no BD e renderiza o html com informacoes dela
def selecionar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    lista_respostas = pergunta.resposta_set.all()
    context = {'pergunta': pergunta, 'lista_respostas': lista_respostas}    
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

# responsavel por salvar a resposta no BD
def salvar_resposta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    try:
        resposta = pergunta.resposta_set.create(usuario=request.POST['usuario'], texto=request.POST['texto'])
    except (KeyError):
        return HttpResponse("Pergunta nao foi salva")
    return HttpResponseRedirect('/resposta_postada/%s/%s' % (pergunta.id, resposta.id))

# renderiza html com confirmacao que a pergunta foi salva
def confirmar_resposta(request, pergunta_id, resposta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    resposta = pergunta.resposta_set.get(pk=resposta_id)
    context = {'pergunta': pergunta, 'resposta': resposta}    
    return render(request, 'qa/confirmacao_resposta_postada.html', context)

# busca pergunta selecionada no BD e renderiza o html com informacoes dela
def selecionar_resposta(request, resposta_id):
    resposta = get_object_or_404(Resposta, pk=resposta_id)
    pergunta = get_object_or_404(Pergunta, pk=resposta.pergunta.id)
    context = {'pergunta': pergunta, 'resposta': resposta}    
    return render(request, 'qa/resposta_selecionada.html', context)

# responsavel por deletar a pergunta selecionada do BD
def deletar_resposta(request, resposta_id):
    resposta = get_object_or_404(Resposta, pk=resposta_id)
    try:
        resposta.delete()
    except (KeyError, resposta.pk != None):
        return HttpResponse("Pergunta nao foi deletada")
    return render(request, 'qa/confirmacao_resposta_deletada.html')

# responsavel por alterar o texto da pergunta selecionada no BD
def alterar_resposta(request, resposta_id):
    resposta = get_object_or_404(Resposta, pk=resposta_id)
    resposta.texto = request.POST['texto_alterado']
    resposta.save()
    context = {'resposta': resposta}    
    return render(request, 'qa/confirmacao_resposta_alterada.html', context)

# renderiza html com o formulario para cadastrar usuarios
def cadastrar_usuario(request):
    return render(request, 'qa/cadastrar_usuario.html')

# responsavel por salvar usuario no BD
def salvar_usuario(request):
    try:
        if Usuario.objects.filter(usuario=request.POST['usuario']):
            return HttpResponse("Usuario ja existe")

        usuario = Usuario(usuario=request.POST['usuario'], senha=request.POST['senha'])
        usuario.save()
    except (KeyError, usuario.pk == None):
        return HttpResponse("Usuario nao foi salva")
    return HttpResponse("Usuario foi cadastrado, olhar no admin")