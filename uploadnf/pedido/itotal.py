import json, requests, urllib
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import math
import http.client

import platform
import os
from dotenv import load_dotenv

load_dotenv()

if platform.system() == 'Windows':
    DJG_SECRET_KEY = os.getenv("ITT_API_KEY_LOCAL")
else:
    DJG_SECRET_KEY = os.getenv("ITT_API_KEY")


uri  = os.getenv("URL_PROJETO") 

#uri = "http://localhost:8000"


#uri = "https://mbp.f3system.com.br"
#uri = "http://mbp.f3system.com.br"
#uri1 = "mbp.f3system.com.br"
#uri1 = uri[7:]


def con_ittProduto(url):
    load_dotenv()

    data_ago = datetime.now()-timedelta(minutes=60)
    #print(data_ago.strftime('%d/%m/%Y %H:%M'))
    new_data = data_ago.strftime("%Y-%m-%d %H:%M")
    
    querystring = {"updated_at__gt": new_data}

    print(querystring)

    #querystring = {"updated_at__gt":"2021-02-12 13:10:00"}
    querystring = {"updated_at__gt":"2021-02-12 13:10:00"}


    headers = {
        'authorization': DJG_SECRET_KEY,
        'cache-control': "no-cache",
        'postman-token': "92d5a133-c9c6-23b2-fd36-4477447770a1"
        }

    #response = requests.request("GET", url, headers=headers, params=querystring)

    response = requests.request("GET", url, headers=headers, params=querystring)

    #print(response.text)

    return response.text

def con_ittCodProd(codprod):
    load_dotenv()
    url = uri + "/produtos/"
    
    #data_ago = datetime.now()-timedelta(minutes=60)
    #print(data_ago.strftime('%d/%m/%Y %H:%M'))
    #new_data = data_ago.strftime("%Y-%m-%d %H:%M")
    
    querystring = {"codprod": codprod}

    print(querystring)

    #querystring = {"updated_at__gt":"2021-02-12 13:10:00"}
    #uerystring = {"updated_at__gt":"2021-02-12 13:10:00"}


    headers = {
        'authorization': DJG_SECRET_KEY,
        'cache-control': "no-cache",
        'postman-token': "92d5a133-c9c6-23b2-fd36-4477447770a1"
        }

    #response = requests.request("GET", url, headers=headers, params=querystring)

    print(" url, headers, querystring ***********>>>>>>"  , url, headers, querystring)
    
    
    response = requests.request("GET", url, headers=headers, params=querystring)

    #print(response.text)

    return response.text


'''
def con_ittPedidos(periodo, db):

    print("periodo  --->", periodo)

    load_dotenv()
    url1 = db
    #print("db ------->>>>", db)
    url = uri + url1
    #print("url ====http://localhost:8000---------------> ", url)
    #exit(12)

    data_ago = datetime.now()-timedelta(minutes=60)
    #print(data_ago.strftime('%d/%m/%Y %H:%M'))
    new_data = data_ago.strftime("%Y-%m-%d %H:%M")
    
    #querystring = {"updated_at__gt": new_data}
    querystring = {"updated_at__gt": periodo}

    #print("querystring====>", querystring)

    #querystring = {"updated_at__gt":"2021-02-12 13:10:00"}
    #querystring = {"updated_at__gt":"2021-02-12 13:10:00"}


    headers = {
        'authorization': DJG_SECRET_KEY,
        'cache-control': "no-cache",
        'postman-token': "92d5a133-c9c6-23b2-fd36-4477447770a1"
        }

    




    #response = requests.request("GET", url, headers=headers, params=querystring)

    print("url====>", url)
    print("headers=====>", headers)
    print("querystring=====>", querystring)

    
    #response = requests.request("GET", url, headers=headers, params=querystring)
    response = requests.request("GET", url, headers=headers)

    data = json.loads(response.text)

    #print("data=========>>>>>3>>>>", data)
    #exit(99)

    var = data['count']
    print("var", var)

    pags = var / 100

    tp = math.ceil(pags)


    # inicio ------------------------
    t = 1
    numcod_acum = []
    while t <= tp:
        #conn = http.client.HTTPConnection("localhost:8000/pedidos/")
        conn = http.client.HTTPConnection(uri[7:])
        #conn = http.client.HTTPSConnection(uri1)

        print("uri===>", uri)
        print("uri1===>", uri[7:])
        #print("******conn== Resultado de conn ==>", conn)
        #exit(90)


        print("******conn== Resultado de conn ==>", conn)




        headers = {
            'authorization': DJG_SECRET_KEY,
            'cache-control': "no-cache",
            'postman-token': "ad5384f1-0540-e0c3-a422-ac5972010ee3"
            }
       

        #url_complemento = "/pedidos/?page={}".format(t)
        url_complemento =  db + "?page={}".format(t)
        print("url_complemento", url_complemento)
        
        
        conn.request("GET", url_complemento, headers=headers)


        print("url complemento + headers =====>" ,url_complemento, headers)


        res = conn.getresponse()
        print("res====>", res)
        data = json.loads(res.read())

        print("data", data)
        #exit(98)

 
        for j in data['results']:
            numcod_acum.append(j['numpedcli'])


        t = t + 1
    return(numcod_acum)

    
    # fim ------------------------'''



def con_ittPedidos(periodo, db):

    print("periodo  --->", periodo)

    load_dotenv()
    url1 = db
    #print("db ------->>>>", db)
    url = uri + url1
    #print("url ====http://localhost:8000---------------> ", url)
    #exit(12)

    data_ago = datetime.now()-timedelta(minutes=60)
    #print(data_ago.strftime('%d/%m/%Y %H:%M'))
    new_data = data_ago.strftime("%Y-%m-%d %H:%M")
    
    #querystring = {"updated_at__gt": new_data}
    querystring = {"updated_at__gt": periodo}

    print("querystring====>", querystring)

    #querystring = {"updated_at__gt":"2021-02-12 13:10:00"}
    #querystring = {"updated_at__gt":"2021-02-12 13:10:00"}


    headers = {
        'authorization': DJG_SECRET_KEY,
        'cache-control': "no-cache",
        'postman-token': "92d5a133-c9c6-23b2-fd36-4477447770a1"
        }

    




    #response = requests.request("GET", url, headers=headers, params=querystring)

    print("url====>", url)
    print("headers=====>", headers)
    print("querystring=====>", querystring)

    
    #response = requests.request("GET", url, headers=headers, params=querystring)
    response = requests.request("GET", url, headers=headers)

    print("response====>", response)
    exit(99)

    data = json.loads(response.text)

    #print("data=========>>>>>3>>>>", data)
    #exit(99)

    var = data['count']
    print("var", var)

    pags = var / 100

    tp = math.ceil(pags)


    # inicio ------------------------
    t = 1
    numcod_acum = []
    while t <= tp:
        #conn = http.client.HTTPConnection("localhost:8000/pedidos/")
        conn = http.client.HTTPConnection(uri[7:])
        #conn = http.client.HTTPSConnection(uri1)

        print("uri===>", uri)
        print("uri1===>", uri[7:])
        #print("******conn== Resultado de conn ==>", conn)
        #exit(90)


        print("******conn== Resultado de conn ==>", conn)




        headers = {
            'authorization': DJG_SECRET_KEY,
            'cache-control': "no-cache",
            'postman-token': "ad5384f1-0540-e0c3-a422-ac5972010ee3"
            }
       

        #url_complemento = "/pedidos/?page={}".format(t)
        url_complemento =  db + "?page={}".format(t)
        print("url_complemento", url_complemento)
        
        
        conn.request("GET", url_complemento, headers=headers)


        print("url complemento + headers =====>" ,url_complemento, headers)


        res = conn.getresponse()
        print("res====>", res)
        data = json.loads(res.read())

        #print("data", data['numpedcli'])
        #exit(98)

 
        for j in data['results']:
            numcod_acum.append(j['numpedcli'])


        t = t + 1
    return(numcod_acum)

# para fazer importação de Pedidos
def con_ittPedidosNew(page):

    #print("periodo  --->", periodo)

    load_dotenv()
    #url1 = db
    #print("db ------->>>>", db)
    #url = uri + url1
    #print("url ====http://localhost:8000---------------> ", url)
    #exit(12)

    data_ago = datetime.now()-timedelta(hours=120)
    #print(data_ago.strftime('%d/%m/%Y %H:%M'))
    new_data = data_ago.strftime("%Y-%m-%d %H:%M")
    
    #querystring = {"updated_at__gt": new_data}
    querystring = {"updated_at__gt": new_data}

    print("querystring====>", querystring)

    #querystring = {"updated_at__gt":"2021-02-12 13:10:00"}
    #querystring = {"updated_at__gt":"2021-02-12 13:10:00"}


    headers = {
        'authorization': DJG_SECRET_KEY,
        'cache-control': "no-cache"
        }

    




    #response = requests.request("GET", url, headers=headers, params=querystring)

    #print("url====>", url)
    print("headers=====>", headers)
    print("querystring=====>", querystring)

    
    #response = requests.request("GET", url, headers=headers, params=querystring)
    #response = requests.request("GET", url, headers=headers)

    #data = json.loads(response.text)

    #print("data=========>>>>>3>>>>", data)
    #exit(99)

    #var = data['count']
    #print("var", var)

    #pags = var / 100

    #tp = math.ceil(pags)


    # inicio ------------------------
    t = 1
    numcod_acum = []
    url = f'http://34.194.18.67/pedidos/pedidos/?page={page}'
    print("url dentro list_notasFiscais_disp====>", url)

    if page == 'all':
        print("imprimir page depois do if e antes de falar que é = a 1 .........>>>", page)
        page = 1
        all_notasFiscais = {'results': {'pedidos': []}}

        while True:

            url = f'http://34.194.18.67/pedidos/pedidos/?page={page}'
            print("url ----> ", url)
            
            
            
            pedidos = requests.get(url, headers=headers, params=querystring)
            data = json.loads(pedidos.text)

            #print(notas)
            #print("data==>", data)
            
            #xit(88)

            try:
                pagina = data['results']
                print("achei a pagina ", page)
                page += 1
                for item in pagina:
                    all_notasFiscais['results']['pedidos'].append(item)
                    
                    numcod_acum.append(item['numpedcli'])

            except KeyError:
                break 
    
    
        x = 0
        for ddbase in all_notasFiscais['results']['pedidos']:
            x = x + 1
            print("print x ------------->", x)
            print("valor de x ", x)
            print("ddbase ====>>", ddbase['numpedcli'])
            

        print("numcod_acum =====> ", numcod_acum )
        return numcod_acum
    
    pedidos = requests.get(url, headers=headers, params=querystring)
    return pedidos  



    '''
    while t <= tp:
        #conn = http.client.HTTPConnection("localhost:8000/pedidos/")
        conn = http.client.HTTPConnection(uri[7:])
        #conn = http.client.HTTPSConnection(uri1)

        print("uri===>", uri)
        print("uri1===>", uri[7:])
        #print("******conn== Resultado de conn ==>", conn)
        #exit(90)


        print("******conn== Resultado de conn ==>", conn)




        headers = {
            'authorization': DJG_SECRET_KEY,
            'cache-control': "no-cache",
            'postman-token': "ad5384f1-0540-e0c3-a422-ac5972010ee3"
            }
       

        #url_complemento = "/pedidos/?page={}".format(t)
        url_complemento =  db + "?page={}".format(t)
        print("url_complemento", url_complemento)
        
        
        conn.request("GET", url_complemento, headers=headers)


        print("url complemento + headers =====>" ,url_complemento, headers)


        res = conn.getresponse()
        print("res====>", res)
        data = json.loads(res.read())

        #print("data", data['numpedcli'])
        #exit(98)

 
        for j in data['results']:
            numcod_acum.append(j['numpedcli'])


        t = t + 1
    return(numcod_acum)'''

# para fazer importação de nota fiscal complemento
def con_ittPedidos_new(page):

    #print("periodo  --->", page)

    load_dotenv()
    DJG_SECRET_KEY = os.getenv("ITT_API_KEY")

    #############################################################################################################
    # Provisório , para testes
    # Provisóriamente para teste , estou fazendo timedelta em horas 

    data_ago = datetime.now()-timedelta(hours=72)
    print("data_ago----->", data_ago)
    
    # 60 minutos antes
    # data_ago = datetime.now()-timedelta(minutes=60)
    #print(data_ago.strftime('%d/%m/%Y %H:%M'))
    ###########################################


    # data_ago = datetime.now()-timedelta(minutes=240)
    #print(data_ago.strftime('%d/%m/%Y %H:%M'))
    new_data = data_ago.strftime("%Y-%m-%d %H:%M:%S")
    #%d/%m/%Y %H:%M:%S
    #querystring = {"updated_at__gt": new_data}
    querystring = {"updated_at__gt": new_data}
    
    # querystring = {"updated_at__gt": new_data, "status": 6}

    print("querystring====>", querystring)


    headers = {
        'authorization': DJG_SECRET_KEY,
        'cache-control': "no-cache"
        }
    
    #response = requests.request("GET", url, headers=headers, params=querystring)

    
    print("headers=====>", headers)
    print("querystring=====>", querystring)

    numcod_acum = []
    url = f'http://34.194.18.67/pedidos/notasfiscais/?page={page}'
    print("url dentro list_notasFiscais_disp====>", url)

    if page == 'all':
        print("imprimir page depois do if e antes de falar que é = a 1 .........>>>", page)
        page = 1
        all_notasFiscais = {'results': {'notasfiscais': []}}

        while True:

            url = f'http://34.194.18.67/pedidos/notasfiscais/?page={page}'
            print("url ----> ", url)
            
            
            
            notas = requests.get(url, headers=headers, params=querystring)
            data = json.loads(notas.text)

            #print(notas)
            #print("data==>", data)
            
            #xit(88)

            try:
                pagina = data['results']
                print("achei a pagina ", page)
                page += 1
                for item in pagina:
                    all_notasFiscais['results']['notasfiscais'].append(item)
                    
                    numcod_acum.append(item['numpedcli'])

            except KeyError:
                break 
    
    
        x = 0
        for ddbase in all_notasFiscais['results']['notasfiscais']:
            x = x + 1
            print("print x ------------->", x)
            print("valor de x ", x)
            print("ddbase ====>>", ddbase['numpedcli'])
            

        print("numcod_acum =====> ", numcod_acum )
        return numcod_acum
    
    notas = requests.get(url, headers=headers, params=querystring)
    return notas  




