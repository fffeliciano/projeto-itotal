import os, sys

projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)


#import json 
from uploadnf.pedido import testarPost
from uploadnf.pedido.itotal import con_ittPedidos
import re
import json, requests, urllib

from dotenv import load_dotenv
import time
from datetime import datetime, timedelta, date
from decimal import Decimal

import logging

logger = logging.getLogger(__name__)

logger.info("teste de passagem importarPedidos - 0")


load_dotenv()
BLING_SECRET_KEY = os.getenv("BLING_API_KEY")

db = "/pedidos/pedidos/"
#date_inicio_itt = "2022-05-30"

#retorno_djg = con_ittPedidos(date_inicio_itt, db)
#pdd_ittset = set(retorno_djg)

situacao_id= "9"

#lista_pdd_bling = []

#nr_pdd = "007464"

url = f"https://bling.com.br/Api/v2/pedido/008513/json/"



#payload = {
#    "apikey": BLING_SECRET_KEY,
#    "filters": f"dataAlteracao[{periodo1} TO {periodo2}]; \
#    idSituacao[{situacao_id}]",
#}

payload = {
        "apikey": BLING_SECRET_KEY,
        }


response = requests.get(url, params=payload)


dados = json.loads(response.content)
print(dados)
with open('./uploadnf/log/dados_blind_teste.json', 'a', encoding='utf-8') as f:
    f.write(json.dumps(dados, ensure_ascii=False))



