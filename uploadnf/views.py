from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage

# Create your views here.
from uploadnf.fornecedor.lernfentrada import lerxml

# ----**************************************************************
#from uploadnf.pedido.lerEtiquetas import lerEtiquetas
from uploadnf.pedido.lerEtiquetas_vv import lerEtiquetas
from uploadnf.pedido.uploadEtiquetas_shopee import lerEtiquetas_shopee
from uploadnf.pedido.uploadEtiquetas_ml import lerEtiquetas_ml
from uploadnf.pedido.uploadEtiquetas_ml_novo import lerEtiquetas_ml_novo
from uploadnf.pedido.uploadEtiquetas_magalu import lerEtiquetas_magalu
from uploadnf.pedido.uploadEtiquetas_magalu_color import lerEtiquetas_magalu_color
from uploadnf.pedido.uploadEtiquetas_magalu_correios import lerEtiquetas_magalu_correios
from uploadnf.pedido.uploadEtiquetas_magalu_correios_novo import lerEtiquetas_magalu_correios_novo
# ----**************************************************************

from uploadnf.fornecedor.nfentrada import gerarNFentrada

from fornecedor.models import NotasFiscais, RetItens, RetornoItensNFEntrada

from pedidos.models import *
from separacao.models import *
from estoque.models import Estoque, Itens

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from produtos.models import Produtos
from produtos.serializers import ProdutosSerializer


import time
from rest_framework import status
from rest_framework.response import Response

#from uploadnf.itotal import con_ittCodProd

import json, requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from django.utils.timezone import get_current_timezone


from uploadnf.produtos.prodPost import produtoPost, prodPostEnviar
from uploadnf.fornecedor.nfePost import notaFiscalPost, notaFiscalPostEnviar


from uploadnf.pedido.pddPost import pedidoPost, pedidoPostEnviar, cancelarPedidoPost,  cancelarPedidoPostEnviar
#
#  Opção para rodar sem enviar etiquetas. comentar a linha de cima e descomentar a linha de baixo
#  precisa gerar um arquivo com numero da nf.txt e salvar em etiquetas/4101.txt
#
#from uploadnf.pedido.pddPost_OLD import pedidoPost, pedidoPostEnviar, cancelarPedidoPost,  cancelarPedidoPostEnviar


from uploadnf.pedido.pnfPost import pddNotaFiscalPost, pddNotaFiscalPostEnviar

#from rest_framework.decorators import api_view

#from rest_framework.decorators import api_view, permission_classes
#from rest_framework.permissions import IsAuthenticated
from .produtos.forms import ProdForm
from django.contrib import messages

from django.core.paginator import Paginator

from fornecedor.forms import RetornoItensNFEntradaForm

from django.template.loader import render_to_string

import logging

logger = logging.getLogger(__name__)


MAX_RETRIES = 5

load_dotenv()
DJG_SECRET_KEY = os.getenv("ITT_API_KEY")

#uri = "http://localhost:8000/"
#uri = "https://mbp.f3system.com.br"
uri = "http://mbp.f3system.com.br"


#== Home =============================================================================
@login_required
def Home(request): 
    count = User.objects.count()   
    return render(request, 'sites/home.html', {
        'count': count
    })






#== Produto ===========================================================================
@login_required
def Produto(request): 

    search = request.GET.get('search')
    

    if search:
        prods = Produtos.objects.filter(nomeprod__icontains=search)
    else:

        prod_list = Produtos.objects.all()   
        
        paginator = Paginator(prod_list, 100)

        page = request.GET.get('page')

        prods = paginator.get_page(page)

    return render(request, 'sites/prodenv.html', {'prods': prods}) 
@login_required
def Produto_html(request): 
    prod = Produtos.objects.all()
    return render(request, 'sites/produto.html', {'prod': prod})  
@login_required
def newprod(request):
    if request.method == 'POST':
        form = ProdForm(request.POST)

        if form.is_valid():
            prod = form.save(commit=False)
            prod.status = 'pass-Ativo'
            prod.save()
            #return redirect('')
            return redirect('material')
    form = ProdForm()
    return render(request, 'sites/newprod.html', {'form': form})

@login_required
def editProd(request,codprod):
    prod = get_object_or_404(Produtos, pk=codprod)
    form = ProdForm(instance=prod)

    if(request.method == 'POST'):
        form = ProdForm(request.POST, instance=prod)

        if(form.is_valid()):
            prod.save()
            return redirect('material')
        else:
            return render(request, 'sites/editprod.html', {'form': form, 'prod': prod} )
    
    else:
        return render(request, 'sites/editprod.html', {'form': form, 'prod': prod} )




@login_required
def delProd(request,codprod):
    prod = get_object_or_404(Produtos, pk=codprod)
    prod.delete()

    messages.info(request, "Tarefa deletada com sucesso.")
    return redirect('material')

# exportar produto para SerraPark
@login_required
def extprod(request, codprod):
    attempt_num = 0  # keep track of how many times we've retried
    while attempt_num < MAX_RETRIES:


        #load_dotenv()
        url = uri + "/produtos/"
        
        #ITT_SECRET_KEY = os.getenv("ITT_API_KEY")

       # cod = request.POST.get("codprod")
        cod = codprod

        querystring = {"codprod": cod}

        print("---- Print querystring ------ ", querystring)
        time.sleep(3) # Sleep for 3 seconds
        
        headers = {
            'authorization': DJG_SECRET_KEY,
            'cache-control': "no-cache",
            'postman-token': "624a8ec7-4292-7f59-b4ef-3a1557a194b4"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        r = response
        if r.status_code == 200:
            data = r.json()
            # return Response(data, status=status.HTTP_200_OK)

            dados_base = produtoPost(data)

            dados_retorno = prodPostEnviar(dados_base)

          #  return render(request, 'sites/produto.html',{} )
            #return render(request, 'Produto/',{} )
            #return redirect('Produto/')
            return redirect('material')


        else:
                    attempt_num += 1
                    print("erro no if r.status_code ** views.py linha 172 ***")
                    # You can probably use a logger to log the error here
                    time.sleep(5)  # Wait for 5 seconds before re-trying 
        
        #return Response(data, template_name='produto.html')
        
    return Response({"error": "Request failed"}, status=r.status_code)

#--  Estoque  ---------------------------------------------------------------------------------
@login_required
def estoqueLog(request): 
    cd = Itens.objects.all()
    return render(request, 'estoque_corpem_list.html', {'cd': cd})  




#--  Estoque  ---------------------------------------------------------------------------------

#== Fornecedor =============================================================================
@login_required
def Fornecedor(request): 
    notas = NotasFiscais.objects.all()   
    #return render(request, 'sites/list.html', {'notas': notas})   
    return render(request, 'sites/list.html', {'notas': notas})  

# menu Upload NF
@login_required
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        #print("---uploaded_file--->>> ", uploaded_file)

        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        #print(uploaded_file.name)
        #print(uploaded_file.size)

        #print("início do lerxml")
        doc = lerxml(uploaded_file)
        #print("-----type doc ----", type(doc))
        #print("fim do lerxml")

        #print("início gerarNFentrada")
        data = gerarNFentrada(doc)

        #print("fim do gerarNFentrada")

    return render(request, 'sites/upload.html')

# menu Lista nf
@login_required
def nf(request): 
    data_atual = datetime.now(tz=get_current_timezone())
    last_month = data_atual - timedelta(days=90)
    nfs = NotasFiscais.objects.filter(updated_at__range=(last_month, data_atual))   
    return render(request, 'nf_list.html', {'nfs': nfs})  

#--- início nf exportar -----------------------------------------------------------
@login_required
def nf_exporta(request, id):
    attempt_num = 0  # keep track of how many times we've retried
    while attempt_num < MAX_RETRIES:


        #load_dotenv()
        url = uri + "/fornecedor/nfe/" + str(id)
        print("url=====>", url)
         
        #ITT_SECRET_KEY = os.getenv("ITT_API_KEY")

        headers = {
            'authorization': DJG_SECRET_KEY,
            'cache-control': "no-cache",
            'postman-token': "624a8ec7-4292-7f59-b4ef-3a1557a194b4"
            }

        response = requests.request("GET", url, headers=headers)
        r = response

        if r.status_code == 200:
            data = r.json()

            dados_base = notaFiscalPost(data)
            
            dados_retorno = notaFiscalPostEnviar(dados_base)

            return redirect('nf')


        else:
                    attempt_num += 1
                    print("erro no if r.status_code ** views.py linha 172 ***")
                    # You can probably use a logger to log the error here
                    time.sleep(5)  # Wait for 5 seconds before re-trying 
        
        #return Response(data, template_name='produto.html')
        
    return Response({"error": "Request failed"}, status=r.status_code)
#--- fim nf exportar -----------------------------------------------------------







# Lista Retorno NFE (tfaa)

def tfaa(request): 
    data_atual = datetime.now(tz=get_current_timezone())
    last_month = data_atual - timedelta(days=90)
    tfaas = RetornoItensNFEntrada.objects.filter(updated_at__range=(last_month, data_atual))   
    return render(request, 'tfaa_list.html', {'tfaas': tfaas})  

def tfaa_update(request, id):
    tfaa = get_object_or_404(RetItens, pk=id)
    if request.method == 'POST':
        form = RetornoItensNFEntradaForm(request.POST, instance=tfaa )
    else:
        form = RetornoItensNFEntradaForm(instance=tfaa)
    return save_tfaa_form(request, form, 'tfaa/partial_tfaa_update.html')


def save_tfaa_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        
        if form.is_valid():
            data_atual = datetime.now(tz=get_current_timezone())
            last_month = data_atual - timedelta(days=90)
            form.save()
            data['form_is_valid'] = True
            tfaas = RetItens.objects.filter(updated_at__range=(last_month, data_atual))
            data['html_tfaa_list'] = render_to_string('tfaa/partial_tfaa_list.html', 
                {'tfaas': tfaas })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

# menu Enviar Nota Fiscal
def Fornecedor_html(request): 
    prod = NotasFiscais.objects.all()
    #return render(request, 'sites/produto.html', {'prod': prod})  
    return render(request, 'sites/fornecedor.html', {})  



# Menu Lista de Pedidos 
@login_required
def pdd(request): 
    data_atual = datetime.now(tz=get_current_timezone())
    last_month = data_atual - timedelta(days=180)
    pds = Pedidos.objects.filter(updated_at__range=(last_month, data_atual))   
    return render(request, 'pdd_list.html', {'pds': pds})  

# pdd exporta -----------------------------------------------------------------------início--------------------
@login_required
def pdd_exporta(request, numpedcli):
    attempt_num = 0  # keep track of how many times we've retried
    while attempt_num < MAX_RETRIES:


        #load_dotenv()
        url = uri + "/pedidos/pedidos/" + str(numpedcli)
        #print("url=====>", url)
         
        #ITT_SECRET_KEY = os.getenv("ITT_API_KEY")

        headers = {
            'authorization': DJG_SECRET_KEY,
            'cache-control': "no-cache",
            'postman-token': "624a8ec7-4292-7f59-b4ef-3a1557a194b4"
            }

        response = requests.request("GET", url, headers=headers)
        print(response.status_code)

        r = response


        if r.status_code == 200:
            data = r.json()
#            dados_base = pedidoPost(data)



            if os.path.exists(f'etiquetas/{data["numnf"]}.txt'):
            
                logger.info("arquivo encontrado!!!!")

                dados_base = pedidoPost(data)

                dados_retorno = pedidoPostEnviar(dados_base)

                return redirect('pdd')

            else:
                logger.warning("Não localizou o arquivo nr(pedido).txt que contem o Pedido = {a}".format(a=str(numpedcli)))
                #logger.warning("Não localizou o arquivo nr ")
                # modelo : logger.info("name_file--> {a} ".format(a=name_file))
    


        else:
                    attempt_num += 1
                    logger.warning("erro no if r.status_code ** views.py linha 419 ***")
                    # You can probably use a logger to log the error here
                    time.sleep(5)  # Wait for 5 seconds before re-trying 
        
        #return Response(data, template_name='produto.html')
        
    return Response({"error": "Request failed"}, status=r.status_code)    

# pdd exporta -----------------------------------------------------------------------fim--------------------


# Etiquetas inicio -----------------------------------------------------------------------------------------

#@login_required
def etiquetas(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print("---uploaded_file--->>> ", uploaded_file)

        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        print(uploaded_file.name)
        print(uploaded_file.size)

        # exit(98)

        # colocar aqui os programas diferentes de upload
        # separando por html e pdf

        arquivo, extensao = os.path.splitext('meuarquivo.txt')

        # exit(90)
        # HTML
        #print("início do lerxml")
        doc = lerEtiquetas(uploaded_file)


        logger.info("doc--> {a} ".format(a=uploaded_file))


        #print("-----type doc ----", type(doc))
        #print("doc ---->", doc)
        #print("fim do etiquetas")

        #print("início gerarNFentrada")
      #  data = gerarNFentrada(doc)

        #print("fim do gerarNFentrada")

    return render(request, 'sites/etiquetas.html')




# Etiquetas fim --------------------------------------------------------------------------------------------

# Etiquetas Shopee início ----------------------------------------------------------------------------------

#@login_required
def etiquetas_shopee(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        logger.info("uploaded_file {a} ".format(a=uploaded_file))
        logger.info("uploaded_file.name {a} ".format(a=uploaded_file.name))
        
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        logger.info("conteudo uploaded_file.name - {a} ".format(a=uploaded_file.name))
        logger.info("uploaded_file.size - {a} ".format(a=uploaded_file.size))

        cwd = os.getcwd()
        logger.info("diretorio atual 2>>> - {a} ".format(a=cwd))

        doc = lerEtiquetas_shopee("xml/" + uploaded_file.name)


        logger.info("doc--> {a} ".format(a=uploaded_file))



    return render(request, 'sites/etiquetas.html')


# Etiquetas Shopee fim -------------------------------------------------------------------------------------



# Etiquetas Mercado Livre início --------------------------------------------------------------------------

#@login_required
def etiquetas_ml(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        logger.info("uploaded_file {a} ".format(a=uploaded_file))
        logger.info("uploaded_file.name {a} ".format(a=uploaded_file.name))
        
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        logger.info("conteudo uploaded_file.name - {a} ".format(a=uploaded_file.name))
        logger.info("uploaded_file.size - {a} ".format(a=uploaded_file.size))

        cwd = os.getcwd()
        logger.info("diretorio atual ml 3>>> - {a} ".format(a=cwd))

        doc = lerEtiquetas_ml("xml/" + uploaded_file.name)


        logger.info("doc--> {a} ".format(a=uploaded_file))



    return render(request, 'sites/etiquetas.html')

# Etiquetas Mercado Livre fim ------------------------------------------------------------------------------


# Etiquetas Mercado Livre Novo início --------------------------------------------------------------------------

#@login_required
def etiquetas_ml_novo(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        logger.info("uploaded_file {a} ".format(a=uploaded_file))
        logger.info("uploaded_file.name {a} ".format(a=uploaded_file.name))
        
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        logger.info("conteudo uploaded_file.name - {a} ".format(a=uploaded_file.name))
        logger.info("uploaded_file.size - {a} ".format(a=uploaded_file.size))

        cwd = os.getcwd()
        logger.info("diretorio atual ml 3>>> - {a} ".format(a=cwd))

        doc = lerEtiquetas_ml_novo("xml/" + uploaded_file.name)


        logger.info("doc--> {a} ".format(a=uploaded_file))



    return render(request, 'sites/etiquetas.html')

# Etiquetas Mercado Livre Novo fim ------------------------------------------------------------------------------




# Etiquetas magalu início ----------------------------------------------------------------------------------

#@login_required
def etiquetas_magalu(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        #print("---uploaded_file--->>> ", uploaded_file)
        logger.info("uploaded_file {a} ".format(a=uploaded_file))
        logger.info("uploaded_file.name {b} ".format(b=uploaded_file.name))

        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        logger.info("uploaded_file.name - {c} ".format(c=uploaded_file.name))
        logger.info("uploaded_file.size - {d} ".format(d=uploaded_file.size))

        cwd = os.getcwd()
        logger.info("diretorio atual 2>>> - {x} ".format(x=cwd))


        logger.info("doc--> {z} ".format(z=uploaded_file.name))

        doc = lerEtiquetas_magalu("xml/" + uploaded_file.name)
        
        logger.info("doc--> {t} ".format(t=uploaded_file))


    return render(request, 'sites/etiquetas.html')


# Etiquetas magalu fim -------------------------------------------------------------------------------------



# Etiquetas Magalu color inicio ----------------------------------------------------------------------------

#@login_required
def etiquetas_magalu_color(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        #print("---uploaded_file--->>> ", uploaded_file)
        logger.info("uploaded_file {a} ".format(a=uploaded_file))
        logger.info("uploaded_file.name {b} ".format(b=uploaded_file.name))

        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        logger.info("uploaded_file.name - {c} ".format(c=uploaded_file.name))
        logger.info("uploaded_file.size - {d} ".format(d=uploaded_file.size))

        cwd = os.getcwd()
        logger.info("diretorio atual 2>>> - {x} ".format(x=cwd))


        logger.info("doc--> {z} ".format(z=uploaded_file.name))

        doc = lerEtiquetas_magalu_color("xml/" + uploaded_file.name)
        
        logger.info("doc--> {t} ".format(t=uploaded_file))


    return render(request, 'sites/etiquetas.html')

# Etiquetas Magalu color fim--------------------------------------------------------------------------------


# Etiquetas Magalu correios inicio ----------------------------------------------------------------------------

#@login_required
def etiquetas_magalu_correios(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        #print("---uploaded_file--->>> ", uploaded_file)
        logger.info("uploaded_file {a} ".format(a=uploaded_file))
        logger.info("uploaded_file.name {b} ".format(b=uploaded_file.name))

        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        logger.info("uploaded_file.name - {c} ".format(c=uploaded_file.name))
        logger.info("uploaded_file.size - {d} ".format(d=uploaded_file.size))

        cwd = os.getcwd()
        logger.info("diretorio atual 2>>> - {x} ".format(x=cwd))


        logger.info("doc--> {z} ".format(z=uploaded_file.name))

        doc = lerEtiquetas_magalu_correios("xml/" + uploaded_file.name)
        
        logger.info("doc--> {t} ".format(t=uploaded_file))


    return render(request, 'sites/etiquetas.html')

# Etiquetas Magalu correios fim--------------------------------------------------------------------------------


# Etiquetas Magalu correios novo inicio ----------------------------------------------------------------------------

#@login_required
def etiquetas_magalu_correios_novo(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        #print("---uploaded_file--->>> ", uploaded_file)
        logger.info("uploaded_file {a} ".format(a=uploaded_file))
        logger.info("uploaded_file.name {b} ".format(b=uploaded_file.name))

        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        logger.info("uploaded_file.name - {c} ".format(c=uploaded_file.name))
        logger.info("uploaded_file.size - {d} ".format(d=uploaded_file.size))

        cwd = os.getcwd()
        logger.info("diretorio atual 2>>> - {x} ".format(x=cwd))


        logger.info("doc--> {z} ".format(z=uploaded_file.name))

        doc = lerEtiquetas_magalu_correios_novo("xml/" + uploaded_file.name)
        
        logger.info("doc--> {t} ".format(t=uploaded_file))


    return render(request, 'sites/etiquetas.html')

# Etiquetas Magalu correios novo fim--------------------------------------------------------------------------------


# pnf exporta (Pedido de Nota Fiscal) ------------------------------------------------------------inicio----






# Menu Lista de Pedidos 

"""
def pnf(request): 
    data_atual = datetime.now(tz=get_current_timezone())
    last_month = data_atual - timedelta(days=30)
    notas = NotasFiscaisSaida.objects.filter(updated_at__range=(last_month, data_atual))   
    return render(request, 'pdd_list.html', {'pds': pds})  
    #return render(request, 'nota_list.html', {'notas': notas})  
"""
# pdd exporta -----------------------------------------------------------------------início--------------------


# exporta do pedido a Nota fiscal para CORPEM
# @login_required
def pnf_exporta(request, codNfSerie):
    attempt_num = 0  # keep track of how many times we've retried
    while attempt_num < MAX_RETRIES:

        #print("--- request e codNFSerie ----->>", request, codNfSerie)
        #load_dotenv()
        #exit(42)


        url = uri + "/pedidos/notasfiscais/" + str(codNfSerie) + "/"
        #print("url=====>", url)
         
        #ITT_SECRET_KEY = os.getenv("ITT_API_KEY")

        headers = {
            'authorization': DJG_SECRET_KEY,
            'cache-control': "no-cache",
            'postman-token': "624a8ec7-4292-7f59-b4ef-3a1557a194b4"
            }

        response = requests.request("GET", url, headers=headers)
        #print(response.status_code)

        r = response
        dd = r.text
        print(dd)

        

        if r.status_code == 200:
            data = r.json()


            dados_base = pddNotaFiscalPost(data)


           
            
            print("dados_base------------------>", dados_base)
            

            #exit(36)

            dados_retorno = pddNotaFiscalPostEnviar(dados_base)

            #exit(34)

            return redirect('nota')


        else:
                    attempt_num += 1
                    print("erro no if r.status_code ** views.py linha 172 ***")
                    # You can probably use a logger to log the error here
                    time.sleep(5)  # Wait for 5 seconds before re-trying 
        
        #return Response(data, template_name='produto.html')
        
    return Response({"error": "Request failed"}, status=r.status_code)    


# pnf exporta (Pedido de Nota Fiscal) ------------------------------------------------------------fim----

"""
# exporta do pedido a Nota fiscal para CORPEM
def pnf_exporta(request, numpedcli):
    attempt_num = 0  # keep track of how many times we've retried
    while attempt_num < MAX_RETRIES:


        #load_dotenv()
        url = uri + "/pedidos/notasfiscais/" + str(numpedcli)
        #print("url=====>", url)
         
        #ITT_SECRET_KEY = os.getenv("ITT_API_KEY")

        headers = {
            'authorization': DJG_SECRET_KEY,
            'cache-control': "no-cache",
            'postman-token': "624a8ec7-4292-7f59-b4ef-3a1557a194b4"
            }

        response = requests.request("GET", url, headers=headers)
        print(response.status_code)

        r = response



        if r.status_code == 200:
            data = r.json()


            dados_base = pddNotaFiscalPost(data)
            
            print("dados_base------------------>", dados_base)
            

            

            dados_retorno = pddNotaFiscalPostEnviar(dados_base)

            return redirect('nota')


        else:
                    attempt_num += 1
                    print("erro no if r.status_code ** views.py linha 172 ***")
                    # You can probably use a logger to log the error here
                    time.sleep(5)  # Wait for 5 seconds before re-trying 
        
        #return Response(data, template_name='produto.html')
        
    return Response({"error": "Request failed"}, status=r.status_code)    


# pnf exporta (Pedido de Nota Fiscal) ------------------------------------------------------------fim----
"""




# pnf_cancela ( Cancelar pedido ) ----------------------------------------------------------------início-
#pnf_cancela

def pnf_cancela(request, numpedcli):
    attempt_num = 0  # keep track of how many times we've retried
    while attempt_num < MAX_RETRIES:


        #load_dotenv()
        url = uri + "/pedidos/pedidos/" + str(numpedcli)
        #print("url=====>", url)
         
        #ITT_SECRET_KEY = os.getenv("ITT_API_KEY")

        headers = {
            'authorization': DJG_SECRET_KEY,
            'cache-control': "no-cache",
            'postman-token': "624a8ec7-4292-7f59-b4ef-3a1557a194b4"
            }

        response = requests.request("GET", url, headers=headers)
        print(response.status_code)

        r = response


        if r.status_code == 200:
            data = r.json()



            print("data---- oi Fernando --------->", data)


            dados_base = cancelarPedidoPost(data)
            
            print("dados_base------------------>", dados_base)
            

            #exit(28)

            dados_retorno = cancelarPedidoPostEnviar(dados_base)

            return redirect('pdd')


        else:
                    attempt_num += 1
                    print("erro no if r.status_code ** views.py linha 172 ***")
                    # You can probably use a logger to log the error here
                    time.sleep(5)  # Wait for 5 seconds before re-trying 
        
        #return Response(data, template_name='produto.html')
        
    return Response({"error": "Request failed"}, status=r.status_code)  


# pnf_cancela ( Cancelar pedido ) ----------------------------------------------------------------início-

# Nota Fiscal -------------------------------------------------------------------------início

def nota(request): 
    data_atual = datetime.now(tz=get_current_timezone())
    last_month = data_atual - timedelta(days=120)
    notas = NotasFiscaisSaida.objects.filter(updated_at__range=(last_month, data_atual))   
    return render(request, 'nota_list.html', {'notas': notas})  



# Nota Fiscal -------------------------------------------------------------------------fim

# Separação de produtos ----------------------------------------------------------------início-
#

#    path('separar/', views.separar, name='separar'),
#    path('separar/<int:numpedcli>/', views.separar_enviar, name='separar'),
def separar(request): 
    data_atual = datetime.now(tz=get_current_timezone())
    last_month = data_atual - timedelta(days=30)
    #notas = Separacao.objects.filter(updated_at__range=(last_month, data_atual))   
    pdds = Separacao.objects.all()
    return render(request, 'separacao_list.html', {'pdds': pdds})  

#
# Separação de produtos ------------------------------------------------------------------- fim --


# Embarques ---------------------------------------------------------------------------- início --
#

def embarque(request): 
    data_atual = datetime.now(tz=get_current_timezone())
    last_month = data_atual - timedelta(days=30)
    #notas = Separacao.objects.filter(updated_at__range=(last_month, data_atual))   
    pdds = Embarque.objects.all()
    return render(request, 'embarque_list.html', {'pdds': pdds})  




#
# Embarques ------------------------------------------------------------------------------- fim --




#== Login Logout ==========================================================================
# menu login e logout
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })
    
@login_required
def secret_page(request):
    return render(request, 'sites/secret_page.html')


class SecretPage(LoginRequiredMixin, TemplateView):
    template_name1 = 'sites/secret_page.html'





#==  Estoque ===============================================================================

#==  indefinido ============================================================================



""" def notas(request): 
    notas = NotasFiscais.objects.all()   
    return render(request, 'notas/nf_list.html', {'notas': notas})  
 """

""" def notaView(request, id):
    nota = get_object_or_404(NotasFiscais, pk=id)
    return render(request, 'sites/nota.html', {'nota': nota})     """

def prodView(request, codprod): 
    prd = get_object_or_404(Produtos, pk=codprod)
    return render(request, 'sites/prodview.html', {'prd': prd})      






""" def posts(request):

    rest = file_pgrm_py.def_enviarPost(sku_Produto)

    #prod = Produtos.objects.all().values()
    
    #main = {'status': True, 'msg': 'OK', 'sites': post_list.data}
    return HttpResponse(prod_list, content_type='application/json')
 """


def enviarProduto(request, codprod):
    prd = get_object_or_404(Produtos, pk=codprod)
    return render(request, 'sites/prodview.html', {'prd': prd})    

""" def enviarNotaFiscal(request, nNF):
    nota = get_object_or_404(NotasFiscais, pk=nNF)
    return render(request, 'sites/prodview.html', {'nota': nota})  """ 






#def Produto_html(request): 
#    prod = Produtos.objects.all()
    #return render(request, 'sites/produto.html', {'prod': prod})  
#    return render(request, 'sites/produto.html', {})  











def external_api_view(request):
    if request.method == "POST":
        attempt_num = 0  # keep track of how many times we've retried
        while attempt_num < MAX_RETRIES:


            #load_dotenv()
            url = uri + "/produtos/"
            
            #ITT_SECRET_KEY = os.getenv("ITT_API_KEY")

            cod = request.POST.get("codprod")

            querystring = {"codprod": cod}
            
            headers = {
                'authorization': DJG_SECRET_KEY,
                'cache-control': "no-cache",
                'postman-token': "624a8ec7-4292-7f59-b4ef-3a1557a194b4"
                }

            response = requests.request("GET", url, headers=headers, params=querystring)
            r = response
            if r.status_code == 200:
                data = r.json()
                #print("data", data)
                #print("results", data)
                #print("len", len(data))
 
                # return Response(data, status=status.HTTP_200_OK)

                #if not 'results' in obj or len(obj['results']) == 0:
                if len(data) == 0:
                    #print("++++ vazio ++++++")
                    #exit(1)
                    #continue
                    return redirect('material')
                else:
                    #print("----- cheio -----")
                    #exit(0)

                
                    dados_base = produtoPost(data)

                    dados_retorno = prodPostEnviar(dados_base)

                return render(request, 'sites/produto.html',{} )

            else:
                        attempt_num += 1
                        print("erro no if r.status_code ** views.py linha 172 ***")
                        # You can probably use a logger to log the error here
                        time.sleep(5)  # Wait for 5 seconds before re-trying """
            
            #return Response(data, template_name='produto.html')
            
        #return Response({"error": "Request failed"}, status=r.status_code)
        print("Request failed")
        return render(request, 'sites/produto.html',{} )
    else:
        #return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)
        print("status=status.HTTP_400_BAD_REQUEST")
        return render(request, 'sites/produto.html',{} )





