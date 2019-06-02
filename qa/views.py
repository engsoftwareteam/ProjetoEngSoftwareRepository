from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .forms import UserForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Pergunta, Resposta, Profile, VotosPerguntas

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
            pergunta = Pergunta(usuario=usuario, titulo=request.POST['titulo'], texto=request.POST['texto'])
            pergunta.save()
        except (KeyError, pergunta.pk == None):
            msg = 'Sua pergunta não foi postada'
            context = {'usuario':usuario, 'msg': msg, 'sucesso':False}
            return render(request, 'qa/postar_pergunta.html', context)
        msg = 'Sua pergunta foi postada'
        context = {'usuario':usuario, 'msg': msg, 'sucesso':True}
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
    VotosTotais = get_list_or_404(VotosPerguntas)
    context = {'pergunta': pergunta, 'lista_respostas': lista_respostas, 'usuario':usuario}#, "VotosTotais": VotosTotais}    
    return render(request, 'qa/pergunta_selecionada.html', context)

# responsavel por deletar a pergunta selecionada do BD
def deletar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    try:
        pergunta.delete()
        msg = "Pergunta deletada com sucesso!"
        sucesso = True
    except (KeyError, pergunta.pk != None):
        msg = "Erro ao deletar pergunta!"
        sucesso = False
    context = {'msg': msg, 'sucesso':sucesso}
    return render(request,'qa/home.html', context)

# responsavel por alterar o texto da pergunta selecionada no BD
def alterar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    pergunta.titulo = request.POST['titulo_alterado']
    pergunta.texto = request.POST['texto_alterado']
    pergunta.save()
    context = {'pergunta': pergunta}
    return HttpResponseRedirect("/selecionar_pergunta/%s" % (pergunta_id))   

# responsavel por salvar a resposta no BD
def postar_resposta(request, pergunta_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            usuario = request.user.get_username()
            pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
            try:
                resposta = pergunta.resposta_set.create(usuario=usuario, texto=request.POST['texto'])
            except (KeyError):
                context = {'msg': "Resposta não foi salva", 'sucesso':False}
                return render(request,'qa/home.html', context)
            return HttpResponseRedirect('/selecionar_pergunta/%s' % (pergunta.id))
        else:
            return HttpResponse("Voce precisa estar logado para postar uma resposta")

# busca pergunta selecionada no BD e renderiza o html com informacoes dela
def selecionar_resposta(request, resposta_id):
    usuario = request.user.get_username()
    if request.method  == 'POST':
        resposta = get_object_or_404(Resposta, pk=resposta_id)
        resposta.texto = request.POST['texto_alterado']
        resposta.save()
        context = {'resposta': resposta, 'usuario': usuario}    
        return HttpResponseRedirect('/selecionar_resposta/%s' % (resposta_id))
    else:
        resposta = get_object_or_404(Resposta, pk=resposta_id)
        pergunta = get_object_or_404(Pergunta, pk=resposta.pergunta.id)
        context = {'pergunta': pergunta, 'resposta': resposta, 'usuario': usuario}    
        return render(request, 'qa/resposta_selecionada.html', context)

# responsavel por deletar a pergunta selecionada do BD
def deletar_resposta(request, resposta_id):
    resposta = get_object_or_404(Resposta, pk=resposta_id)
    try:
        resposta.delete()
        msg = "Resposta deletada com sucesso!"
        sucesso = True
    except (KeyError, resposta.pk != None):
        msg = "Resposta nao foi deletada"
        sucesso = False
    context = {'msg': msg, 'sucesso':sucesso}
    return render(request,'qa/home.html', context)

# responsavel por alterar o texto da pergunta selecionada no BD
def alterar_resposta(request, resposta_id):
    resposta = get_object_or_404(Resposta, pk=resposta_id)
    resposta.texto = request.POST['texto_alterado']
    resposta.save()
    return HttpResponseRedirect('/selecionar_resposta/%s' %(resposta_id))

def logged(request):
    if request.user.is_authenticated:
        context = {'msg': "Você está logado", 'sucesso':True}
        return render(request,'qa/home.html', context)
    else:
        context = {'msg': "Você não está logado", 'sucesso':True}
        return render(request,'qa/home.html', context)

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
                msg = 'Usuário inativo'
                context = {'msg':msg, 'sucesso': False}
                return render(request, 'qa/login.html', context)
        else:
            msg = 'Usuário ou senha incorretos'
            context = {'msg':msg, 'sucesso': False}
            return render(request, 'qa/login.html', context)
    else:
         return render(request, 'qa/login.html')

def logout_usuario(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/home')
    else:
        context = {'msg': "Você não está logado", 'sucesso':False}
        return render(request,'qa/home.html', context)
        

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
            return HttpResponseRedirect('/home')
        else:
            print(user_form.errors)
            context = {'msg': "Não registrado"}
            return render(request,'qa/cadastro.html', context)
    else:
        user_form = UserForm()
        return render(request, 'qa/cadastro.html')

def meu_perfil(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        username = request.user.get_username()
        email = request.POST['email']
        instituicao = request.POST['instituicao']
        profissao = request.POST['profissao']
        descricao = request.POST['descricao']
        user = request.user
        if new_password != '':
            user.set_password(new_password)
            user.save()
            login(request,user)

        profile = Profile.objects.get(user=request.user)
        user.email=email
        user.save()
        profile.instituicao = instituicao
        profile.profissao = profissao
        profile.descricao = descricao
        user.save()
        profile.save()
        return HttpResponseRedirect('/meu_perfil')
    else:
        usuario = request.user.get_username()
        if usuario:
            email = request.user.email
            profile = Profile.objects.get(user=request.user)
            context = {'usuario':usuario, 'email':email, 'profissao':profile.profissao, 'instituicao':profile.instituicao, 'descricao':profile.descricao}
            return render(request, 'qa/meu_perfil.html', context)
        return render(request, 'qa/meu_perfil.html')

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


def remover_usuario(request):
    if request.method == 'POST':
        username = request.user.get_username()
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            user.delete()
            return HttpResponseRedirect('/login_usuario')
        else:
            return HttpResponseRedirect('/meu_perfil')
    else:
        return HttpResponse("veio de um metodo get")

def VotePergunta(request, pergunta_id):
    usuario = request.user.get_username()
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    pergunta.votos = request.POST['votos']
    pergunta.save()
    voto = VotosPerguntas(pergunta = pergunta, usuario = usuario)
    voto.save()
    context = {'pergunta': pergunta, 'voto': voto}
    return HttpResponseRedirect("/selecionar_pergunta/%s" % (pergunta_id)) 
