import os, sys
import json 
import json, requests, urllib
from dotenv import load_dotenv
import time
from datetime import datetime ,timedelta, date



projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

import django





load_dotenv()
DJG_SECRET_KEY = os.getenv("ITT_API_KEY")

import math
import http.client
#from decimal import Decimal

import logging

logger = logging.getLogger(__name__)

logger.info("teste de passagem exportarPedidos - 0")


############################# acessar setting fora do projeto ###############################
import sys
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE','inventario.settings')
django.setup() #run django.setup BEFORE importing modules to setup the environ
#from pedidos.models import Pedidos
from uploadnf.pedido.pddPost import pedidoPost, pedidoPostEnviar
from pedidos.models import Pedidos

#t=Pedidos.objects.all()



#print(t)

#exit(9)
############################# acessar setting fora do projeto ###############################


from uploadnf.pedido import pddPost




x = datetime.now()

if int(x.strftime("%H")) > 2:
    n = 0
else:
    n = 1

date_N_days_ago = datetime.now() - timedelta(days=n)

date_inicio_formated = date_N_days_ago.strftime("%d/%m/%Y")
#print(date_inicio_formated)
#print()
date_fim_formated = datetime.now().strftime("%d/%m/%Y") 
#print(date_fim_formated)
#print()
# data inicio para pesquisa no django drf 
date_inicio_itt = date_N_days_ago.strftime("%Y-%m-%d")


#periodo = []
periodo1 = date_inicio_formated
periodo2 = date_fim_formated



#--------------------------------------------------------------------- excluir/comentar estas linhas
#periodo1 = "02/07/2021"
#periodo2 = "04/07/2021"
#--------------------------------------------------------------------- excluir/comentar estas linhas



#retorno_djg = con_ittPedidos(date_inicio_itt)
#pdd_ittset = set(retorno_djg)
#print("pdd_itt--->", pdd_ittset)

#=============================================================================inicio



load_dotenv()
#url = "https://mbp.f3system.com.br/pedidos/pedidos/"
url = "http://mbp.f3system.com.br/pedidos/pedidos/"

# correto e definitivo
# Está em minutos, que deve ser o correto quando entrar em produção.
#data_ago = datetime.now()-timedelta(minutes=60)

#############################################################################################################
# Provisório , para testes
# Provisóriamente para teste , estou fazendo timedelta em horas 
data_ago = datetime.now()-timedelta(hours=200)
#############################################################################################################


#print(data_ago.strftime('%d/%m/%Y %H:%M'))
new_data = data_ago.strftime("%Y-%m-%d %H:%M")

#querystring = {"updated_at__gt": new_data}
querystring = {"updated_at__gt": new_data}


#querystring = {"updated_at__gt":"2021-02-12 13:10:00"}
#querystring = {"updated_at__gt":"2021-01-01 13:10:00"}


headers = {
    'authorization': DJG_SECRET_KEY,
    'cache-control': "no-cache",
    'postman-token': "92d5a133-c9c6-23b2-fd36-4477447770a1"
    }



print(headers, querystring)
#exit(90)
response = requests.request("GET", url, headers=headers, params=querystring)



data = json.loads(response.text)

for n in data['results']:
    print(n)


#exit(90)


var = data['count']

pags = var / 100

tp = math.ceil(pags)
print("tp ::>>", tp)
t = 1

numcod_acum = []
url = "http://mbp.f3system.com.br/pedidos/pedidos/?page={}"



while t <= tp:
    #conn = http.client.HTTPConnection("https://mbp.f3system.com.br")
    #conn = http.client.HTTPConnection("http://mbp.f3system.com.br")
    print("antes do try")
    try:
        response = requests.get(url.format(t), headers=headers, params=querystring)
        
        print("url completa", url.format(t))

        print(response.status_code)
        
        dados = json.loads(response.content)
        print("antes do continue")
        
        #continue
        #print("dados ++++>>>>>", dados)

        continue

        #with open('dados_blind_teste.json', 'a', encoding='utf-8') as f:
        #    f.write(json.dumps(dados, ensure_ascii=False))


        if response.status_code == 200:
            #print("status 200")
            dados = json.loads(response.content)
            
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        break
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        break
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        break
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        break

    print("depois do try")





    
    conn.request("GET", bling_complemento, headers=headers)

    res = conn.getresponse()

    data = json.loads(res.read())

    x = 0
    for ddbase in data['results']:
        x = x + 1
        print("print x ------------->", x)

        print("valor de x ", x)

        exit(90)

        dados_base = pedidoPost(ddbase)

        dados_retorno = pedidoPostEnviar(dados_base)


        # t vai somar mais uma pagina com 100 registros.
        t = t + 1

