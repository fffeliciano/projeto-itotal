import requests
import json 
import time
import datetime
#from datetime import date, datetime

import os
from dotenv import load_dotenv

load_dotenv()
DJG_SECRET_KEY = os.getenv("ITT_API_KEY")



def AddBase(dados):

    #print(" -----AddBase--dados---->>>>>", dados)
    time.sleep(2)
    #url = "https://mbp.f3system.com.br/produtos/"
    url = "http://mbp.f3system.com.br/produtos/"
  
    headers = {
        'authorization': DJG_SECRET_KEY,
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "b2bfec68-b95b-6bcc-be4f-f8f63188f00e"
        }

    response = requests.request("POST", url, data=json.dumps(dados), headers=headers)

    #print(dados)
    #print(dados['codprod'])

    x=dados['codprod']
    z=response.status_code
    today = datetime.datetime.now()


    name = "LogProdutos" + str(today) + ".json"
    #print(name)
    

    v= str(today) + " - " + str(z) + " - " +   x +  " - " + response.text

    with open('logProdutos.txt', 'a', encoding="utf-8") as fd:
        
        fd.write(v)
        fd.write("\n")
        if z > 220:
            fd.write(json.dumps(dados))
            fd.write("\n")


    return(response)


def AddBasePedidos(dados):

    #print(" -----AddBasePedidos--dados---->>>>>", dados)
    time.sleep(2)
    #url = "https://mbp.f3system.com.br/pedidos/"
    url = "http://mbp.f3system.com.br/pedidos/"
  
    headers = {
    'authorization': "Token 4e9c2dcad540a9139c79ee6e6a91b0b09d0b467f",
    'content-type': "application/json; charset=UTF-8;",
    'cache-control': "no-cache",
    'postman-token': "f63f85ca-212a-b6c3-0497-7322f53ada91"
    }
  

    response = requests.request("POST", url, data=json.dumps(dados), headers=headers)

    print(response.status_code)

    print("nnnnnnnn json.dumps(dados) nnnnnnnnnn" ,json.dumps(dados))

    print("====Response ===>>", response.status_code)

    x=dados['numpedcli']

    dtlog = datetime.datetime.now().strftime("%Y_%m_%d")
    filename = "LogPedidos"+dtlog+".json"
    

    z=response.status_code
    today = datetime.datetime.now()
    
    v= str(today) + " - " + str(z) + " - " +  x  +  " - " + response.text

    with open(filename, 'a', encoding="utf-8") as fd:
        
        fd.write(v)
        fd.write("\n")
        if z > 220:
            fd.write(json.dumps(dados))
            fd.write("\n")
        

    return(response)


