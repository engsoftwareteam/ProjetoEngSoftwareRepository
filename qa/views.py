from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Usuario, Pergunta, Resposta

# responsavel por salvar a pergunta no BD
def postar_pergunta(request):
    if request.method == 'POST':
        try:
            pergunta = Pergunta(usuario=request.POST['usuario'], texto=request.POST['texto'])
            pergunta.save()
        except (KeyError, pergunta.pk == None):
            return HttpResponse("Pergunta nao foi salva")
        return HttpResponseRedirect('/pergunta_postada/%s' %pergunta.pk)
    else:
        return render(request, 'qa/postar_pergunta.html')

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
def postar_resposta(request, pergunta_id):
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



@login_required
def special(request):
    try:
        return HttpResponse("Voce esta logado")
    except (KeyError):
        return HttpResponse("voce nao esta logado")

@login_required
def logout(request):
    try:
        logout(request)
        return HttpResponse("logout sucesso")
    except (KeyError):
        return HttpResponse("voce nao esta logado")

def registrar_usuario(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'qa/registrar_usuario.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/menu')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Senha ou usuario errado ou nao existe")
    else:
         return render(request, 'qa/login.html')