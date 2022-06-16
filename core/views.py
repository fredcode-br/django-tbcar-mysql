from django.shortcuts import render, redirect
from core.forms import FormCliente, FormFabricante, FormVeiculo, FormTabela, FormRotativo, FormMensalista
from core.models import Cliente, Fabricante, Veiculo, Tabela, Rotativo, Mensalista
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'core/index.html')


class Registrar(generic.CreateView):
    template_name = 'registration/register.html'
    success_url = '/'
    form_class = UserCreationForm


@login_required()
def cadastro_cliente(request):
    try:
        if request.user.is_staff:
            form = FormCliente( request.POST or None, request.FILES or None )
            if form.is_valid():
                nome = form.cleaned_data['nome']
                form.save()
                messages.success(request, f'Cliente { nome } cadastrado com sucesso!')
                return redirect('url_lista_clientes')
            contexto = {'form': form, 'titulo':'Cadastro de Cliente', 'stringBotao':'Cadastrar','url':'/'}
            return render(request, 'core/cadastro.html', contexto)
        else:
            contexto = {'string': 'Voce não tem permissão para executar esta operação. Procure seu chefe.', 'url': '/'}
            return render(request, 'core/mensagem.html', contexto)
    except:
        messages.erro(request, f'Não foi possível executar esta operação')
        return redirect('url_lista_clientes')

@login_required()
def lista_clientes(request):
    if request.user.is_staff:
        string = ""
        if request.POST:
            if request.POST['i_pesquisa']:
                dados = Cliente.objects.filter(nome=request.POST['i_pesquisa'])
                if len(dados) == 0:
                     string= ("Nenhum registro encontrado")
            else:
                dados = Cliente.objects.all()
        else:
            dados = Cliente.objects.all()
        contexto = {'dados': dados, 'string': string}
        return render(request, 'core/lista_clientes.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def cadastro_veiculo(request):
    if request.user.is_staff:
        form = FormVeiculo ( request.POST or None, request.FILES or None)
        if form.is_valid():
            placa = form.cleaned_data['placa']
            form.save()
            messages.success(request, f'Veículo {placa} cadastrado com sucesso!')
            return redirect ('url_lista_veiculos')
        contexto = {'form': form, 'titulo':'Cadastro de Veiculo', 'stringBotao':'Cadastrar','url':'/'}
        return render (request, 'core/cadastro.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def lista_veiculos(request):
    if request.user.is_staff:
        dados = Veiculo.objects.all()
        if request.POST:
            if request.POST['i_pesquisa']:
                dados = Veiculo.objects.filter(modelo=request.POST['i_pesquisa'])
        contexto = {'dados': dados}
        return render(request, 'core/lista_veiculos.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)




@login_required()
def cadastro_fabricante (request):
    if request.user.is_staff:
        form = FormFabricante(request.POST or None)
        if form.is_valid():
            marca = form.cleaned_data['descricao']
            form.save()
            messages.success(request, f'Fabricante { marca } cadastrado com sucesso!')
            return redirect('url_lista_fabricantes')
        contexto = {'form': form, 'titulo':'Cadastro de Fabricante', 'stringBotao':'Cadastrar', 'url':'/'}
        return render(request, 'core/cadastro.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)

@login_required()
def lista_fabricantes (request):
    if request.user.is_staff:
        dados = Fabricante.objects.all()
        if request.POST:
            if request.POST['i_pesquisa']:
                dados = Fabricante.objects.filter(descricao=request.POST['i_pesquisa'])

        contexto = {'dados': dados}
        return render(request, 'core/lista_fabricantes.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)

@login_required()
def altera_cliente (request, id):
    if request.user.is_staff:
        objeto = Cliente.objects.get(id=id)
        form = FormCliente(request.POST or None, request.FILES or None, instance=objeto)
        form.fields ['email'].widget.attrs['readonly'] = True
        if form.is_valid():
            nome = form.cleaned_data['nome']
            form.save()
            messages.success(request, f'Dados do cliente { nome } atualizados com sucesso!' )
            return redirect('url_lista_clientes')
        contexto = {'form': form, 'titulo': 'Alteração de cliente', 'stringBotao':'Salvar', 'url': '/lista_clientes/', 'formAtualiza' : True}
        return render(request, 'core/cadastro.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def exclua_cliente (request, id):
    if request.user.is_staff:
        objeto = Cliente.objects.get(id=id)
        #confirmar se pode mesmo excluir (manda pro html de confirmacao)
        if request.POST:
            objeto.delete()
            messages.success(request, f'Dados do cliente { objeto.nome } excluídos com sucesso!')
            return redirect('url_lista_clientes')
        contexto={'objeto':objeto.nome, 'url':'/lista_clientes'}
        return render(request, 'core/confirma_exclusao.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def altera_veiculo(request, id):
    if request.user.is_staff:
        objeto=Veiculo.objects.get(id=id)
        form=FormVeiculo(request.POST or None, request.FILES or None, instance=objeto)
        form.fields['id_cliente'].widget.attrs['readonly'] = True
        form.fields['id_fabricante'].widget.attrs['readonly'] = True
        form.fields['placa'].widget.attrs['readonly'] = True
        form.fields['modelo'].widget.attrs['readonly'] = True
        contexto = {'form': form,  'string': f'Dados de {objeto.modelo} salvos', 'url': '/lista_veiculos', 'stringBotao':'Salvar', 'formAtualiza' : True}
        if form.is_valid():
            placa = form.cleaned_data['placa']
            form.save()
            messages.success(request, f'Dados do veículo { placa } atualizados com sucesso!')
            return redirect('url_lista_veiculos')
        contexto = {'form': form, 'titulo': 'Alteração de veículo', 'stringBotao':'Salvar', 'url': '/lista_veiculos/', 'formAtualiza' : True}
        return render(request,'core/cadastro.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def exclua_veiculo (request, id):
    if request.user.is_staff:
        objeto = Veiculo.objects.get(id=id)
        #se veio por request.POST, o usuário clicou em SIM
        if request.POST:
            objeto.delete()
            messages.success(request, f'Dados do veiculo {objeto.placa} excluidos com sucesso!')
            return redirect('url_lista_veiculos')
        contexto={'objeto':objeto.modelo, 'url':'/lista_veiculos', 'stringBotao': 'Excluir'}
        return render(request, 'core/confirma_exclusao.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def altera_fabricante (request, id):
    if request.user.is_staff:
        objeto=Fabricante.objects.get(id=id)
        form=FormFabricante(request.POST or None, instance=objeto)
        contexto ={'form': form,  'string': f'Dados de {objeto.descricao} salvos', 'url':'/lista_fabricantes','stringBotao':'Salvar', 'formAtualiza' : True}
        if form.is_valid():
            marca = form.cleaned_data['descricao']
            form.save()
            messages.success(request, f'Fabricante { marca } atualizado com sucesso!')
            return redirect('url_lista_fabricantes')
        contexto = {'form': form, 'titulo': 'Alteração de fabricante', 'stringBotao':'Salvar', 'url': '/lista_fabricantes/', 'formAtualiza' : True}
        return render(request,'core/cadastro.html',contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def exclua_fabricante (request, id):
    if request.user.is_staff:
        objeto = Fabricante.objects.get(id=id)
        if request.POST:
            objeto.delete()
            messages.success(request, f'Fabricante {objeto.descricao} excluido com sucesso!')
            return redirect('url_lista_fabricantes')
        contexto={'objeto':objeto.descricao, 'url':'/lista_fabricantes', 'stringBotao': 'Excluir'}
        return render (request,'core/confirma_exclusao.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def cadastro_tabela (request):
    if request.user.is_staff:
        form = FormTabela (request.POST or None)
        if form.is_valid():
            item = form.cleaned_data['descricao']
            form.save()
            messages.success(request, f'Valor de { item } cadastrado com sucesso!')
            return redirect('url_lista_tabela')
        contexto = {'form': form, 'titulo':'Cadastro de valor', 'stringBotao':'Cadastrar','url':'/'}
        return render(request, 'core/cadastro.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def lista_tabela(request):
    dados = Tabela.objects.all()
    contexto = {'dados': dados}
    return render(request, 'core/tabela.html', contexto)


@login_required()
def altera_tabela (request, id):
    if request.user.is_staff:
        objeto=Tabela.objects.get(id=id)
        form=FormTabela(request.POST or None, instance=objeto)
        contexto ={'form': form, 'string': f'Dados de {objeto.descricao} salvos', 'url': '/lista_tabela','stringBotao': 'Salvar'}
        if form.is_valid():
            item = form.cleaned_data['descricao']
            form.save()
            messages.success(request, f'Valor de { item } atualizado com sucesso!')
            return redirect('url_lista_tabela')
        contexto = {'form': form, 'titulo': 'Alteração de valor', 'stringBotao':'Salvar', 'url': '/lista_tabela/', 'formAtualiza' : True}
        return render(request,'core/cadastro.html',contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/', 'formAtualiza' : True}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def exclua_tabela (request, id):
    if request.user.is_staff:
        objeto = Tabela.objects.get(id=id)
        if request.POST:
            objeto.delete()
            messages.success(request, f'Dados do item {objeto.descricao} excluidos com sucesso!')
            return redirect('url_lista_tabela')
        contexto={'objeto': objeto.descricao, 'url': '/lista_tabela/', 'stringBotao': 'Excluir'}
        return render (request,'core/confirma_exclusao.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def cadastro_rotativo (request):
    if request.user.is_staff:
        form = FormRotativo(request.POST or None)
        if form.is_valid():
            veiculo = form.cleaned_data['id_veiculo']
            form.save()
            messages.success(request, f'Veículo { veiculo } cadastrado com sucesso!')
            return redirect('url_lista_rotativos')
        contexto = {'form': form, 'titulo':'Cadastro de Rotativo', 'stringBotao':'Cadastrar', 'dateTime': True, 'url': '/'}
        return render(request, 'core/cadastro.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def atualiza_rotativo (request, id):
    if request.user.is_staff:
        obj = Rotativo.objects.get(id=id)
        form = FormRotativo(request.POST or None, instance=obj)
        if form.is_valid():
            if obj.calcula_Total():
                veiculo = form.cleaned_data['id_veiculo']
                form.save()
                messages.success(request, f'Dados do veículo { veiculo } atualizados com sucesso!')
                return redirect('url_lista_rotativos')
                contexto = {'form': form, 'titulo': 'Alteração de rotativo', 'stringBotao':'Salvar', 'url': '/lista_rotativos/', 'formAtualiza' : True}
            else:
            # VER ATUALIZACAO SEM INDICAR O HORARIO DE SAIDA
                contexto = {'string': 'Data de saída inválida!'}
                return render (request, 'core/mensagem.html', contexto)
            return redirect('url_lista_rotativos')
        contexto = {'form': form, 'titulo':'Atualização de rotativo', 'stringBotao':'Atualizar', 'url': '/lista_rotativos/', 'dateTime': True, 'formAtualiza' : True}
        return render(request, 'core/cadastro.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def exclua_rotativo(request, id):
    if request.user.is_staff:
        objeto = Rotativo.objects.get(id=id)
        if request.POST:
            objeto.delete()
            messages.success(request, f'Dados do veiculo {objeto.id_veiculo} excluidos com sucesso!')
            return redirect('url_lista_rotativos')
        contexto={'objeto': objeto.id_veiculo, 'url': '/lista_rotativos', 'stringBotao': 'Excluir'}
        return render (request,'core/confirma_exclusao.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def lista_rotativos(request):
    if request.user.is_staff:
        dados = Rotativo.objects.all()
        if request.POST:
            if request.POST['i_pesquisa']:
                dados = Rotativo.objects.filter(id_veiculo=request.POST['i_pesquisa'])
        contexto = {'dados': dados}
        return render (request, 'core/lista_rotativos.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def cadastro_mensalista (request):
   if request.user.is_staff:
       form = FormMensalista(request.POST or None)
       if form.is_valid():
           veiculo = form.cleaned_data['id_veiculo']
           form.save()
           messages.success(request, f'Veículo { veiculo } cadastrado com sucesso!')
           return redirect('url_lista_mensalistas')
       contexto = {'form': form, 'titulo':'Cadastro de Mensalista', 'stringBotao':'Cadastrar', 'url':'/'}
       return render(request, 'core/cadastro.html', contexto)
   else:
       contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
       return render(request, 'core/mensagem.html', contexto)


@login_required()
def atualiza_mensalista (request, id):
    if request.user.is_staff:
        obj = Mensalista.objects.get(id=id)
        form = FormMensalista(request.POST or None, instance=obj)
        if form.is_valid():
            obj.calcula_desconto()
            veiculo = form.cleaned_data['id_veiculo']
            form.save()
            messages.success(request, f'Dados do veículo { veiculo } atualizados com sucesso!')
            return redirect('url_lista_mensalistas')

        contexto = {'form': form, 'titulo':'Atualização de Mensalista', 'stringBotao':'Atualizar', 'url': '/lista_mensalistas/', 'formAtualiza' : True}
        return render(request, 'core/cadastro.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/', 'formAtualiza' : True}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def exclua_mensalista(request, id):
    if request.user.is_staff:
        objeto = Mensalista.objects.get(id=id)
        if request.POST:
            objeto.delete()
            messages.success(request, f'Dados do veiculo {objeto.id_veiculo} excluidos com sucesso!')
            return redirect('url_lista_mensalistas')
        contexto={'objeto': objeto.id_veiculo, 'url': '/lista_mensalistas', 'stringBotao': 'Excluir'}
        return render (request,'core/confirma_exclusao.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)


@login_required()
def lista_mensalistas(request):
    if request.user.is_staff:
        dados = Mensalista.objects.all()
        if request.POST:
            if request.POST['i_pesquisa']:
                dados = Rotativo.objects.filter(id_veiculo=request.POST['i_pesquisa'])
        contexto = {'dados': dados}
        return render (request, 'core/lista_mensalistas.html', contexto)
    else:
        contexto = {'string': 'Voce não tem permissao para executar esta operação. Procure seu chefe.', 'url': '/'}
        return render(request, 'core/mensagem.html', contexto)
