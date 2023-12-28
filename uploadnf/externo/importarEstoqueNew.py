import json 
from uploadnf.pedido import testarPost
from uploadnf.pedido.itotal import con_ittPedidos
import re
import json, requests, urllib
import os
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta, date
from decimal import Decimal
import http.client

load_dotenv()
BLING_SECRET_KEY = os.getenv("BLING_API_KEY")

#----------------------------------------------

conn = http.client.HTTPConnection("serrapark.dd.spiritlinux.com:81")

payload = "{\"CORPEM_ERP_ESTOQUE\": {\"CGCCLIWMS\": \"35457333000129\"}}"

headers = {
    'content-type': "application/json",
    'accept-language': "pt-BR",
    'cache-control': "no-cache",
    'postman-token': "d7ab735e-463a-7838-2f82-a846930d4942"
    }

conn.request("POST", "/scripts/mh.dll/wc", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

dados = json.loads(data.decode("utf-8"))

print("dados======>", dados)

#exit(67)


class Estoque(object):

    def __init__(self, nome_atualizacao):
        self.nome_atualizacao = nome_atualizacao


    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<sku {self.id}>'     



class Itens(object):
    #def __init__(self, desconto, observacoes, observacaointerna, data, numero, numeroOrdemCompra, vendedor, valorfrete, totalprodutos, totalvenda, situacao, dataSaida, loja, numeroPedidoLoja, tipoIntegracao, cliente, nota  , transporte, itens, parcelas):
    def __init__(self, cd, ft, qc, qb, qf):
    #def __init__(self, codigo, quantidade):
        self.cd = cd
        self.ft = ft
        self.qc = qc
        self.qb = qb
        self.qf = qf
            
    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<codigo do produto {self.cd}>'


# checar aqui se a lista de numero de pedido tem algum registo no Model do Django pdd_ittset (Linha 45)


###################################
###################################

#####>>>>>>> continua Aqui!!
print("continua aqui!!! ----1-----")



today = datetime.now()
    
v= "Atualizado em: " + str(today)





dd_pedido ={}
#pedido = u['pedido']
dd_pedido['nome_atualizacao'] = v

print('-- dd_pedido ----->', json.dumps(dd_pedido))


dd_item_acumulado = []

u = dados['CORPEM_ERP_ESTOQUE']['PRODUTOS']
print("---  u  --------->", u)

dd_item = {}
dd_item['cd'] = u['CD']
dd_item['ft'] = u['FT']
dd_item['qc'] = u['QC']
dd_item['qb'] = u['QB']
dd_item['qf'] = u['QF']

    
#Decimal(valorunidade.replace(',','.'))

#print("valor dd_item['vlr_unit']---->", dd_item['vlr_unit'])
#print("valor dd_item['vlr_unit']---->", c_item['valorunidade'])


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

print( "dd item ------>", json.dumps(dd_item))

#c =  json.dumps(j['item'])

its = Itens.from_json(json.dumps(dd_item))

#print(its)

jsonStrIts = json.dumps(its.__dict__)

JsonDictIts = json.loads(jsonStrIts)

dd_item_acumulado.append(JsonDictIts)


#print("-----------------JsonDictIts--------------", JsonDictIts)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#pedd = Estoque.from_json(i)
pedd = Estoque.from_json(json.dumps(dd_pedido))

#its = Itens.from_json(i)

jsonStr = json.dumps(pedd.__dict__)

#jsonStrIts = json.dumps(its.__dict__)


jsonDict = json.loads(jsonStr)

#JsonDictIts = json.loads(jsonStrIts)

myDict3 = {}
myDict3["itens"] = dd_item_acumulado

#print("mmmmmmmm myDict3 mmmmmmmmm", myDict3)


jsonDict.update(myDict3)

print("############## jsonDict ###############" , json.dumps(jsonDict))

#exit(6)


resultado_retorno = testarPost.AddEstoque(jsonDict)
#resultado_retorno = testarPost.AddBasePAddBasePedidosedidos(jsonDict)

print("#######  resultado_retorno ########", resultado_retorno)

#n = n+1
