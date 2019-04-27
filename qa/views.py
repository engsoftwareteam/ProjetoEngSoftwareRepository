from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .forms import UserForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Pergunta, Resposta, Profile

def home(request):
    if request.user.is_authenticated:
        usuario = request.user.get_username()
    else:
        usuario = None
    context = {'usuario': usuario}
    return render(request, 'qa/home.html', context)

# responsavel por salvar a pergunta no BD
def postar_pergunta(request):
    usuario = request.user.get_username()
    if request.method == 'POST':
        try:
            pergunta = Pergunta(usuario=usuario, texto=request.POST['texto'])
            pergunta.save()
        except (KeyError, pergunta.pk == None):
            return HttpResponse("Pergunta nao foi salva")
        msg = 'sua pergunta foi postada'
        context = {'usuario':usuario, 'msg': msg}
        return render(request, 'qa/postar_pergunta.html', context)
    else:
        context = {"usuario": usuario}
        return render(request, 'qa/postar_pergunta.html', context)
    
# renderiza html com a lista de perguntas ja feitas
def listar_perguntas(request):
    usuario = request.user.get_username()
    perguntas = get_list_or_404(Pergunta)
    context = {'perguntas': perguntas, 'usuario':usuario}
    return render(request, 'qa/lista_perguntas.html', context)

# busca pergunta selecionada no BD e renderiza o html com informacoes dela
def selecionar_pergunta(request, pergunta_id):
    usuario = request.user.get_username()
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    lista_respostas = pergunta.resposta_set.all()
    context = {'pergunta': pergunta, 'lista_respostas': lista_respostas, 'usuario':usuario}    
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
    if request.method == 'POST':
        usuario = None
        if request.user.is_authenticated:
            usuario = request.user.get_username()
            pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
            try:
                resposta = pergunta.resposta_set.create(usuario=usuario, texto=request.POST['texto'])
            except (KeyError):
                return HttpResponse("Pergunta nao foi salva")
            return HttpResponseRedirect('/selecionar_pergunta/%s' % (pergunta.id))
        else:
            return HttpResponse("Voce precisa estar logado para postar uma resposta")

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

def logged(request):
    if request.user.is_authenticated:
        return HttpResponse("voce esta logado")
    else:
        return HttpResponse("voce nao esta logado")

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/home')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            msg = 'Usuário ou senha incorretos'
            context = {'msg':msg}
            return render(request, 'qa/login.html', context)
    else:
         return render(request, 'qa/login.html')

def logout_usuario(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/home')
    else:
        return HttpResponse("voce nao esta logado")
        

def registrar_usuario(request):
    # Retirado o userInfo
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_profile = ProfileForm(data=request.POST)
        if user_form.is_valid() and user_profile.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = user_profile.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponse('Registrado com sucesso')
        else:
            print(user_form.errors)
            return HttpResponse('Nao foi registrado')
    else:
        user_form = UserForm()
        return render(request, 'qa/cadastro.html')


# renderiza html com a lista de perguntas ja feitas
def meus_posts(request):
    usuario = request.user.get_username()
    perguntas = None
    respostas = None
    if Pergunta.objects.filter(usuario=usuario).exists():
        perguntas = Pergunta.objects.filter(usuario=usuario)

    if Resposta.objects.filter(usuario=usuario).exists():
        respostas = Resposta.objects.filter(usuario=usuario)

    context = {'perguntas': perguntas, 'respostas': respostas, 'usuario':usuario}
    return render(request, 'qa/meus_posts.html', context)

def alterar_senha(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        user = authenticate(username=username, password=old_password)
        if user:
            if user.is_active:
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                else:
                    return HttpResponse("Confirm your password again.")
                return HttpResponseRedirect('/login_usuario')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return HttpResponse("Try again.")
    else:
        return render(request, 'qa/alterar_senha.html')

def remover_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            user.delete()
            return HttpResponseRedirect('/menu')
        else:
            return HttpResponse("Usuario não existe")
    else:
        return render(request, 'qa/remover_usuario.html')
