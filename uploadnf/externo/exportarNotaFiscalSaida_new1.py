import os, sys
import json, requests, urllib
from dotenv import load_dotenv
from datetime import datetime ,timedelta, date

import math
import http.client
#from decimal import Decimal

projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

import django

load_dotenv()
DJG_SECRET_KEY = os.getenv("ITT_API_KEY")

import logging

logger = logging.getLogger(__name__)

logger.info("teste de passagem exportarPedidos - 0")

############################# acessar setting fora do projeto ###############################

os.environ.setdefault('DJANGO_SETTINGS_MODULE','inventario.settings')
django.setup() #run django.setup BEFORE importing modules to setup the environ
from pedidos.models import NotasFiscaisSaida
#from uploadnf.pedido.pddPost import pedidoPost, pedidoPostEnviar
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



#############################################################################################################
# Provisório , para testes
# Provisóriamente para teste , estou fazendo timedelta em horas 
data_ago = datetime.now()-timedelta(hours=72)
print("data_ago----->", data_ago)
#############################################################################################################


#print(data_ago.strftime('%d/%m/%Y %H:%M'))
new_data = data_ago.strftime("%Y-%m-%d %H:%M")

#querystring = {"updated_at__gt": new_data}
querystring = {"updated_at__gt": new_data, "status": 6}


#print("querystring======>", querystring)
#querystring = {"updated_at__gt":"2021-02-12 13:10:00"}
#querystring = {"updated_at__gt":"2021-02-12 13:10:00"}


headers = {
    'authorization': DJG_SECRET_KEY,
    'cache-control': "no-cache"
    }
#print("headers ---->" , headers )

#exit(88)
#response = requests.request("GET", url, headers=headers, params=querystring)

# ip da f3c =       34.194.18.67

def list_notasFiscais(page=1):
    url = f'http://34.194.18.67/pedidos/notasfiscais/?page={page}'

    if page == 'all' :
        page = 1
        all_notasFiscais = {'results': {'notasfiscais': []}}

        while True:

            url = f'http://34.194.18.67/pedidos/notasfiscais/?page={page}'
            print("url ----> ", url)
            
            
            
            notasfiscais = requests.get(url, headers=headers, params=querystring)
            data = json.loads(notasfiscais.text)

            #print(notasfiscais)
            #print("data==>", data)
            
            #exit(88)

            try:
                pagina = data['results']
                #print("achei a pagina ", page)
                page += 1
                for item in pagina:
                    all_notasFiscais['results']['notasfiscais'].append(item)
            except KeyError:
                break 
        
        
        x = 0



        for ddbase in all_notasFiscais['results']['notasfiscais']:
            x = x + 1
            print("print x ------------->", x)
            print("valor de x ", x)
            print("ddbase ====>>", ddbase['numpedcli'])
            print("ddbase ====>>", ddbase)

            if ddbase['situacao'] == None:
                print("Registro sem dados da Nota Fiscal")
                continue
            else:
                dados_base = pddNotaFiscalPost(ddbase)
                dados_retorno = pddNotaFiscalPostEnviar(dados_base)




        #---------------------------------------------------------------------------------------------------------------------------------------------------
        return all_notasFiscais
        
        


    notasfiscais = requests.get(url, headers=headers, params=querystring)
    return notasfiscais          







# Testes para produtos
#def test_list_pedidos_response_code_is_200():
#    retorno = list_pedidos()
#    assert retorno.status_code == 200


#def test_list_pedidos_contents():
#    retorno = list_pedidos()
#    assert 'pedidos' in retorno.text

def get_list_all_notasFiscais():
    retorno = list_notasFiscais(page='all')
    assert 'notasfiscais' in retorno['results']
    


retorno = get_list_all_notasFiscais()
