import json, requests, urllib
import os
from dotenv import load_dotenv
from uploadnf.itotal import con_ittCodProd
import datetime
from produtos.models import Produtos


# está recebendo um json


def produtoPost(dados):

    class Produto(object):
        def __init__(self, nomeprod, codprod, iws_erp, tpolret, iautodtven, qtddpzoven, ilotfab, idtfab, idtven, inser, codfab, nomefab, status, embalagens):
            self.CODPROD = codprod
            self.NOMEPROD = nomeprod
            self.TPOLRET = iws_erp
            self.IWS_ERP = tpolret
            self.IAUTODTVE = iautodtven
            self.QTDDPZOVEN = qtddpzoven
            self.ILOTFAB = ilotfab
            self.IDTFAB = idtfab
            self.IDTVEN = idtven
            self.INSER = inser
            self.CODFAB = codfab        
            self.NOMEFAB = nomefab
            #self.updated = updated_at

        @classmethod
        def from_json(cls, json_string):
            # dict
            json_dict = json.loads(json_string)
            return cls(**json_dict)
            
    class Embalagem(object):
        def __init__(self, codunid, fator, codbarra, pesoliq, pesobru, alt, lar, comp, vol):
            self.CODUNID = codunid
            self.FATOR = fator
            self.CODBARRA = codbarra
            self.PESOLIQ = pesoliq
            self.PESOBRU = pesobru
            self.ALT = str(alt)
            self.LAR = str(lar)
            self.COMP = str(comp)
            self.VOL = int(vol)
    
        @classmethod
        def from_json(cls, json_string):
            # dict
            json_dict = json.loads(json_string)
            return cls(**json_dict)

        def __repr__(self):
            return f'<ean {self.CODBARRA}>' 


    dados_dict = {}
    dados_list = []

    print("*** dados que vieram do POST de produto.html ====>", dados)
    print(type(dados))

    #for i in dados['results']:
    for i in dados['results']:        
        dados_dict.update(i)
        print(i)

    print("=== dados_dict ========>", dados_dict)
    print(type(dados_dict))

    prod = Produto.from_json(json.dumps(dados_dict))
    print(" exemplo>> LETRA p ===>", prod)
    print(type(prod))


    for n in dados_dict['embalagens']:
        c =  json.dumps(n)
            
        emb = Embalagem.from_json(c)

        # json
        jsonStrIts = json.dumps(emb.__dict__)
        
        # dict
        JsonDictIts = json.loads(jsonStrIts)

    
    # dict ==> json
    jsonStr = json.dumps(prod.__dict__)

    # json ==> dict
    jsonDict = json.loads(jsonStr)

    myDict3 = {}
    myDict3["EMBALAGENS"] = [JsonDictIts]
    jsonDict.update(myDict3)

    myDict1 = {}
    myDict1["CORPEM_ERP_MERC"] = {"CGCCLIWMS": "38317322000131"}

    myDict2 = {}
    myDict2["PRODUTOS"] = [jsonDict]

    jsonDict.update(myDict3)

    myDict1["CORPEM_ERP_MERC"].update(myDict2)

    print()
    print(json.dumps(myDict1))
    return json.dumps(myDict1)

    
def prodPostEnviar(dados):
    # Início Fase 2
    # Salvar dados de Produtos na CORPEM_ERP  

    #json_dados = '''{"CORPEM_ERP_MERC": {"CGCCLIWMS": "38317322000131", "PRODUTOS": [{"CODPROD": "36692", "NOMEPROD": "APARADOR PHILIPS ONE BLADE QP2510/10", "TPOLRET": "0", "IWS_ERP": "0", "IAUTODTVE": "0", "QTDDPZOVEN": "0", "ILOTFAB": "0", "IDTFAB": "0", "IDTVEN": "0", "INSER": "1", "CODFAB": "19807", "NOMEFAB": "", "EMBALAGENS": [{"CODUNID": "FR", "FATOR": "1", "CODBARRA": "8710103821359", "PESOLIQ": "0.00000", "PESOBRU": "0.00000", "ALT": "", "LAR": "", "COMP": "", "VOL": ""}]}]}}'''
    #json_dados = '''{"CORPEM_ERP_MERC": {"CGCCLIWMS": "38317322000131", "PRODUTOS": [{"CODPROD": "36692", "NOMEPROD": "APARADOR PHILIPS ONE BLADE QP2510/10", "TPOLRET": "0", "IWS_ERP": "0", "IAUTODTVE": "0", "QTDDPZOVEN": "0", "ILOTFAB": "0", "IDTFAB": "0", "IDTVEN": "0", "INSER": "1", "CODFAB": "19807", "NOMEFAB": "", "EMBALAGENS": []}]}}'''


    payload = dados

    #print("----- print(payload ***-*) ------>>", payload)
    #print("-------|codprod|---------", dados.codprod)

    # 38317322000131

    dados_json = json.loads(dados)
    
    for n in dados_json['CORPEM_ERP_MERC']['PRODUTOS']:
        cod_prod = n['CODPROD']


    
    url = "http://serrapark.dd.spiritlinux.com:81/scripts/mh.dll/wc"

    #payload = "{\"CORPEM_ERP_MERC\": {\"CGCCLIWMS\": \"38317322000131\", \"PRODUTOS\": [{\"CODPROD\": \"11106\", \"NOMEPROD\": \"IMPRESSORA EPSON MATRICIAL FX890 BLACK - C11C524142\", \"TPOLRET\": \"0\", \"IWS_ERP\": \"0\", \"IAUTODTVE\": \"0\", \"QTDDPZOVEN\": \"0\", \"ILOTFAB\": \"0\", \"IDTFAB\": \"0\", \"IDTVEN\": \"0\", \"INSER\": \"1\", \"CODFAB\": \"L117079B\", \"NOMEFAB\": \"\", \"EMBALAGENS\": [{\"CODUNID\": \"FR\", \"FATOR\": \"1\", \"CODBARRA\": \"010343913981\", \"PESOLIQ\": \"0.000\", \"PESOBRU\": \"14.000\", \"ALT\": \"18\", \"LAR\": \"44\", \"COMP\": \"36\", \"VOL\": 1}]}]}}"
    headers = {
        'content-type': "application/json; charset=utf-8",
        'cache-control': "no-cache",
        'postman-token': "bd816b6d-e4b5-957b-0028-c47e2ae27fdf"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    #print(response.text.encode('utf-8'))


    if response.status_code == 200:
        #print(" Achou a Pagina retorno 200 ========>)")
        #print(response.text.encode('utf-8'))
        #print(response.json())
        #print()
        if "CORPEM_WS_OK" in response.text:
            print("******* Sucess *******")
            #print()
            prod = Produtos.objects.get(codprod = cod_prod)
            prod.status = "Registrado"
            prod.save()
        else:
            print("#### erro ####",response.text.encode('utf-8'))
            #print()


    filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    #print("----filename1----", filename1)
    filename2 = 'Prod-sku-'+ cod_prod + '-' +filename1+'.json'
    #print("----filename2----", filename2)
 
    with open('uploadnf/log/'+filename2, 'a' , encoding="utf-8" ) as f:
        #f.write(json.dumps(response.text))
        f.write(response.text)
        
        print("salvou....")

    



    
    print('passou por aqui')
       
    return response
    
