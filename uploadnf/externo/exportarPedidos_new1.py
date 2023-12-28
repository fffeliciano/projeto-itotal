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
#**********************************************************************************************************************************************alterar aqui*************************
#from uploadnf.pedido.pddPost import pedidoPost, pedidoPostEnviar
from uploadnf.pedido.pddPost_new1 import pedidoPost, pedidoPostEnviar
#**********************************************************************************************************************************************alterar aqui*************************
from pedidos.models import Pedidos




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




load_dotenv()

# correto e definitivo
#
# Esta em minutos, que deve ser o correto quando entrar em producao.
#data_ago = datetime.now()-timedelta(minutes=60)

#############################################################################################################
# Provisorio , para testes
# Provisoriamente para teste , estou fazendo timedelta em horas 
#data_ago = datetime.now()-timedelta(hours=200)
data_ago = datetime.now()-timedelta(hours=120)
#############################################################################################################


#print(data_ago.strftime('%d/%m/%Y %H:%M'))
new_data = data_ago.strftime("%Y-%m-%d %H:%M")

#querystring = {"updated_at__gt": new_data} ** updated_at__gt (__gt e igual a data maior que:)
querystring = {"updated_at__gt": new_data, "status": 6 }


headers = {
    'authorization': DJG_SECRET_KEY,
    'cache-control': "no-cache"
    }


def list_pedidos(page=1):
    url = f'http://34.194.18.67/pedidos/pedidos/?page={page}'


    if page == 'all' :
        page = 1
        all_pedidos = {'results': {'pedidos': []}}
        

        while True:
            url = f'http://34.194.18.67/pedidos/pedidos/?page={page}'
            print("url ----> ", url)
            
            
            
            pedidos = requests.get(url, headers=headers, params=querystring)
            data = json.loads(pedidos.text)
            

            try:
                pagina = data['results']
                print("achei a pagina ", page)
                page += 1
                for item in pagina:
                    all_pedidos['results']['pedidos'].append(item)
            except KeyError:
                break 
  

        x = 0
        for ddbase in all_pedidos['results']['pedidos']:
            x = x + 1
            #print("print x ------------->", x)
            #print("valor de x ", x)
            #print("ddbase ====>>", ddbase['numpedcli'])
            #print("ddbase ====>>", ddbase)

            #continue
            #exit(90)

            dados_base = pedidoPost(ddbase)

            #print("dados_base - conteúdo - =====>>", dados_base)

            #exit(99)

            dados_retorno = pedidoPostEnviar(dados_base)







        #---------------------------------------------------------------------------------------------------------------------------------------------------
        return all_pedidos
    
    
    
    pedidos = requests.get(url, headers=headers, params=querystring)
    return pedidos

    
#retorno = list_pedidos(page='all')



# Testes para produtos
'''def test_list_pedidos_response_code_is_200():
    retorno = list_pedidos()
    assert retorno.status_code == 200


def test_list_pedidos_contents():
    retorno = list_pedidos()
    assert 'pedidos' in retorno.text'''

def test_get_all_pedidos():
    retorno = list_pedidos(page='all')
    assert 'pedidos' in retorno['results']
    


retorno = test_get_all_pedidos()