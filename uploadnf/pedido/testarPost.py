import requests
import json
import time
import datetime
#from datetime import date, datetime

import os
from dotenv import load_dotenv

load_dotenv()
DJG_SECRET_KEY = os.getenv("ITT_API_KEY")
uri  = os.getenv("URL_PROJETO")

#uri = "http://127.0.0.1:8000"
#uri = "https://mbp.f3system.com.br"
#uri = "http://mbp.f3system.com.br"
#uri = "http://localhost:8000"


def AddBase(dados):

    print(" -----AddBase--dados---->>>>>", dados)
    time.sleep(2)
    url = uri + "/produtos/" #"http://localhost:8000/produtos/"
  
    headers = {
        'authorization': DJG_SECRET_KEY,
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "b2bfec68-b95b-6bcc-be4f-f8f63188f00e"
        }

    

    response = requests.request("POST", url, data=json.dumps(dados), headers=headers)

    print(dados)
    print(dados['codprod'])

    x=dados['codprod']
    z=response.status_code
    today = datetime.datetime.now()


    name = "LogProdutos" + str(today) + ".json"
    #print(name)
    
    #----------------------------------------------------------------------------------------------


    dtlog = datetime.datetime.now().strftime("%Y_%m_%d")
    filename = "uploadnf/log/LogProduto"+dtlog+".json"

    v= str(today) + " - " + str(z) + " - " +   x +  " - " + response.text

    with open(filename, 'a', encoding="utf-8") as fd:




    #----------------------------------------------------------------------------------------------
    #v= str(today) + " - " + str(z) + " - " +   x +  " - " + response.text

    #with open('uploadnf/log/' + filename2, 'a' , encoding="utf-8") as f:

    #with open('uploadnf/log/logProdutos.txt', 'a', encoding="utf-8") as fd:
        
        fd.write(v)
        fd.write("\n")
        if z > 220:
            fd.write(json.dumps(dados))
            fd.write("\n")


    return(response)


def AddBasePedidos(dados, db):


    #print(" -----AddBasePedidos--dados---->>>>>", dados)
    #time.sleep(2)

    url1 = db
    url = uri  + url1    # "http://localhost:8000" + url1


    print("url -------http://localhost:8000/pedidos/ ------->  ", url)
    #print("|| ------- db ------->  ", db)
    #exit(95)
  
    headers = {
    'authorization': DJG_SECRET_KEY,
    'content-type': "application/json; charset=UTF-8;",
    'cache-control': "no-cache",
    'postman-token': "f63f85ca-212a-b6c3-0497-7322f53ada91"
    }
  

    print("headers=====>>>", headers)
    
    #exit(97)

    response = requests.request("POST", url, data=json.dumps(dados), headers=headers)

    print(response.status_code)

    print("nnnnnnnn json.dumps(dados) nnnnnnnnnn" ,json.dumps(dados))

    print("====Response ===>>", response.status_code)

    
    #exit(96)

    #db = "/pedidos/pedidos/"
    #db = "/pedidos/notasfiscais/"

    if "notasfiscais" in db:
        x=dados['codNfSerie']
    else:
        x=dados['numpedcli']




    dtlog = datetime.datetime.now().strftime("%Y_%m_%d")

    if 'complemento' in db:
        filename2 = 'complem'
    else:
        filename2 = 'base'

    print("filename2==============>", filename2)


    filename = "uploadnf/log/LogNotasFiscais"+filename2+dtlog+".json"
    

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

#--- Consulta Notas Fiscais -------------------------------------------------------------------------------início

def consultarBaseNFsaida(parametros, db):

    #print(" -----AddBase--dados---->>>>>", dados)
    #time.sleep(2)


    url1 = db

    #url = uri + "/" + url1 + parametros + "/" # "http://localhost:8000/" + url1
    url = uri + url1 + parametros + "/" # "http://localhost:8000/" + url1


    #print("url -------http://localhost:8000/pedidos/ ------->  ", url)
    
    #print("------------- parametros - db -------------->>", parametros, db)
    print("------------- url --------------->>", url)


    
    #exit(97)
    
    
    

    headers = {
        'authorization': DJG_SECRET_KEY,
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "b2bfec68-b95b-6bcc-be4f-f8f63188f00e"
        }


    #response = requests.request("GET", url, data=json.dumps(parametros), headers=headers)
    response = requests.request("GET", url, headers=headers)

    print("--- response ----->>", response)
    print("--- response.text ----->>", response.text)





    return(response.text)

#--- Consulta Notas Fiscais ----------------------------------------------------------------------------------Fim

#--- Update db Notas Fiscais ------------------------------------------------------------------------------início
def UpdateBasePedidos(parametros, dados, db):


    #print(" -----AddBasePedidos--dados---->>>>>", dados)
    #time.sleep(2)

    print("--- parametros dados db ----->>", parametros, dados, db)

    #exit(88)

    url1 = db
    #url = uri  + url1    # "http://localhost:8000" + url1
    url = uri + url1 + parametros + "/" # "http://localhost:8000/" + url1


    #print("url -------http://localhost:8000/pedidos/ ------->  ", url)
    #print("|| ------- db ------->  ", db)

  
    headers = {
    'authorization': DJG_SECRET_KEY,
    'content-type': "application/json; charset=UTF-8;",
    'cache-control': "no-cache",
    'postman-token': "f63f85ca-212a-b6c3-0497-7322f53ada91"
    }
  

    print("headers=====>>>", headers)
    
    #exit(97)

    response = requests.request("PUT", url, data=json.dumps(dados), headers=headers)

    print(response.status_code)

    print("nnnnnnnn json.dumps(dados) nnnnnnnnnn" ,json.dumps(dados))

    print("====Response ===>>", response.status_code)

    
         
    """
    if "notasfiscais" in db:
        x=dados['parametros']
    else:
        x=dados['numpedcli']
    """

    x=parametros



    dtlog = datetime.datetime.now().strftime("%Y_%m_%d")

    if 'complemento' in db:
        filename2 = 'complem'
    else:
        filename2 = 'base'

    print("filename2==============>", filename2)


    filename = "uploadnf/log/LogNotasFiscais"+filename2+dtlog+".json"
    

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

#--- Update db Notas Fiscais ---------------------------------------------------------------------------------Fim

def consultarBase(parametros, db):

    #print(" -----AddBase--dados---->>>>>", dados)
    #time.sleep(2)

    url1 = db

    url = uri + "/" + url1  # "http://localhost:8000/" + url1


    #print("url -------http://localhost:8000/pedidos/ ------->  ", url)
    
    print("------------- url --------------->>", url)
    
    
    
    
    

    headers = {
        'authorization': DJG_SECRET_KEY,
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "b2bfec68-b95b-6bcc-be4f-f8f63188f00e"
        }


    response = requests.request("GET", url, data=json.dumps(parametros), headers=headers)


    print("--------- response ---------->>", response)

    #print(dados)
    #print(dados['codprod'])

    x=dados['codprod']
    z=response.status_code
    today = datetime.datetime.now()
    


    name = "LogProdutos" + str(today) + ".json"
    print(name)
    
    #exit(93)

    v= str(today) + " - " + str(z) + " - " +   x +  " - " + response.text

    with open('uploadnf/log/logProdutos.txt', 'a', encoding="utf-8") as fd:
        
        fd.write(v)
        fd.write("\n")
        if z > 220:
            fd.write(json.dumps(dados))
            fd.write("\n")


    return(response)


#------------------------------------------------------------------------------------

def AddEstoque(dados):
   


    #print(" -----AddBase--dados---->>>>>", dados)
    time.sleep(2)
    url = uri + "/estoque/" # "http://localhost:8000/estoque/"
  
    headers = {
        'authorization': DJG_SECRET_KEY,
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "b2bfec68-b95b-6bcc-be4f-f8f63188f00e"
        }




    response = requests.request("POST", url, data=json.dumps(dados), headers=headers)

   
    
    #print(dados)
    #print(dados['codprod'])

    #x=dados['codprod']
    z=response.status_code
    today = datetime.datetime.now()


    #name = "LogEstoque" + str(today) + ".json"
    #print(name)

    dtlog = datetime.datetime.now().strftime("%Y_%m_%d")
    filename = "uploadnf/log/LogEstoque"+dtlog+".json"
    

    v= str(today) + " - " + str(z) + " - " + " - " + response.text


    #with open('uploadnf/log/' + filename2, 'a' , encoding="utf-8") as f:

    #with open('uplaodnf/log/logEstoque.txt', 'a', encoding="utf-8") as fd:
    #with open('uploadnf/log/logEstoque.txt', 'a', encoding="utf-8") as fd:
    with open(filename, 'a', encoding="utf-8") as fd:
        
        fd.write(v)
        fd.write("\n")
        if z > 220:
            fd.write(json.dumps(dados))
            fd.write("\n")


    return(response)
