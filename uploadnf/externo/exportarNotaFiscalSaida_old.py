import json 
import json, requests, urllib
import os
from dotenv import load_dotenv
import time
from datetime import datetime ,timedelta, date


import math
import http.client
#from decimal import Decimal

load_dotenv()
DJG_SECRET_KEY = os.getenv("ITT_API_KEY")


############################# acessar setting fora do projeto ###############################
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','inventario.settings')

django.setup() #run django.setup BEFORE importing modules to setup the environ
from pedidos.models import NotasFiscaisSaida
from uploadnf.pedido.pddPost import pedidoPost, pedidoPostEnviar
from uploadnf.pedido.pnfPost import pddNotaFiscalPost, pddNotaFiscalPostEnviar

#t=Pedidos.objects.all()

#print(t)

#exit(9)
############################# acessar setting fora do projeto ###############################


from uploadnf.pedido import pnfPost




x = datetime.now()

if int(x.strftime("%H")) > 2:
    n = 0
else:
    n = 1

date_N_days_ago = datetime.now() - timedelta(days=n)

date_inicio_formated = date_N_days_ago.strftime("%d/%m/%Y")
print(date_inicio_formated)
print()
date_fim_formated = datetime.now().strftime("%d/%m/%Y") 
print(date_fim_formated)
print()
# data inicio para pesquisa no django drf 
date_inicio_itt = date_N_days_ago.strftime("%Y-%m-%d")


#periodo = []
periodo1 = date_inicio_formated
periodo2 = date_fim_formated



#--------------------------------------------------------------------- excluir/comentar estas linhas
periodo1 = "08/07/2021"
periodo2 = "08/07/2021"
#--------------------------------------------------------------------- excluir/comentar estas linhas



#retorno_djg = con_ittPedidos(date_inicio_itt)
#pdd_ittset = set(retorno_djg)
#print("pdd_itt--->", pdd_ittset)

#=============================================================================início



load_dotenv()
url = "http://localhost:8000/pedidos/notasfiscais/"




# correto e definitivo
# Está em minutos, que deve ser o correto quando entrar em produção.
#data_ago = datetime.now()-timedelta(minutes=60)

#############################################################################################################
# Provisório , para testes
# Provisóriamente para teste , estou fazendo timedelta em horas 
data_ago = datetime.now()-timedelta(hours=45)
print("data_ago----->", data_ago)
#############################################################################################################


#print(data_ago.strftime('%d/%m/%Y %H:%M'))
new_data = data_ago.strftime("%Y-%m-%d %H:%M")

#querystring = {"updated_at__gt": new_data}
querystring = {"updated_at__gt": new_data}


print("querystring======>", querystring)
#querystring = {"updated_at__gt":"2021-02-12 13:10:00"}
#querystring = {"updated_at__gt":"2021-02-12 13:10:00"}


headers = {
    'authorization': DJG_SECRET_KEY,
    'cache-control': "no-cache",
    'postman-token': "92d5a133-c9c6-23b2-fd36-4477447770a1"
    }


response = requests.request("GET", url, headers=headers, params=querystring)


data = json.loads(response.text)

var = data['count']

pags = var / 100

tp = math.ceil(pags)

t = 1

numcod_acum = []
while t <= tp:
    conn = http.client.HTTPConnection("localhost:8000")

    headers = {
        'authorization': DJG_SECRET_KEY,
        'cache-control': "no-cache",
        'postman-token': "ad5384f1-0540-e0c3-a422-ac5972010ee3"
        }
    

    bling_complemento = "/pedidos/notasfiscais/?page={}".format(t)

       
    conn.request("GET", bling_complemento, headers=headers)

    res = conn.getresponse()

    data = json.loads(res.read())

    print("data=====>",data)

    x = 0
    for ddbase in data['results']:
        x = x + 1
        print("print x ------------->", x)


        dados_base = pddNotaFiscalPost(ddbase)

        dados_retorno = pddNotaFiscalPostEnviar(dados_base)


        # t vai somar mais uma pagina com 100 registros.
        t = t + 1

