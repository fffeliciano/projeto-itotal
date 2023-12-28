import os, sys

projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)


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
logger.info("teste de passagem importarNotaFiscal -  1")




#----------------------------------------------

load_dotenv()
BLING_SECRET_KEY = os.getenv("BLING_API_KEY")

#N = 90

# n numero de dias atras.
n = 1


x = datetime.now()

if x.weekday() == 0:
    n = 5
elif int(x.strftime("%H")) > 14:
    n = 2
else:
    n = 2





#if int(x.strftime("%H")) > 10:
#    n = 0
#else:
#    n = 1



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
periodo1 = "20/10/2022"
periodo2 = "24/11/2022"
#--------------------------------------------------------------------- excluir/comentar estas linhas

print("-- Periodo 1", periodo1)
print("-- Pediodo 2", periodo2)
#exit(96)




db = "/pedidos/notasfiscais/"
retorno_djg = con_ittPedidos(date_inicio_itt, db)
pdd_ittset = set(retorno_djg)
#print("pdd_itt--->", pdd_ittset)

situacao_id= "9"

n = 1
lista_pdd_bling = []
while True:
    url = f"https://bling.com.br/Api/v2/pedidos/page={n}/json/"
    """
    payload = {
        "apikey": BLING_SECRET_KEY,
        "filters": f"dataAlteracao[{periodo1} TO {periodo2}]; \
        idSituacao[{situacao_id}]",
    }
    
    payload = {
        "apikey": BLING_SECRET_KEY,
        "filters": f"dataAlteracao[{periodo1} TO {periodo2}];",
    }
    """

    payload = {
        "apikey": BLING_SECRET_KEY,
        "filters": f"dataEmissao[{periodo1} TO {periodo2}]; \
        idSituacao[{situacao_id}]",
    }
    



    #print("payload---->",   payload)
    



    try:
        response = requests.get(url, params=payload)

        #print(response.status_code)
        
        dados = json.loads(response.content)

        #with open('dados_blind_teste.json', 'a', encoding='utf-8') as f:
        #    f.write(json.dumps(dados, ensure_ascii=False))


        #exit(7)



        if response.status_code == 200:
            #print("status 200")
            dados = json.loads(response.content)
            

            #with open('dados_blind_teste.json', 'a', encoding='utf-8') as f:
            #    f.write(json.dumps(dados, ensure_ascii=False))
            

            #for w in dados['retorno']['pedidos']:
             #   lista_pdd_bling.append(w['pedido']['numero'])

            #print("len nr pedidos :" ,len(dados['retorno']['pedidos']))

            #print(" n ---->", n)
        
            #print('lista_pdd_bling ------>', lista_pdd_bling)

            #print("len nr pedidos incluídos lista", len(lista_pdd_bling))
            

            #with open('dados_localhost_pedidos_teste.json', 'w', encoding='utf-8') as f:
            #   f.write(retorno_djg)


            #print(retorno_djg)

        
    

     
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


    

    data = json.loads(response.content)
    datas = data["retorno"]

    #print("data----->", data)


    if response == 200:
        continue

    if "erros" in datas:
        print("===== achei erro 14 =====>")
        break


    # -> response = requests.get(url, params=payload)
    # -> dados = json.loads(response.content)

    #print("*** Print Dados ****>>>", dados)

    class NotaFiscalSaida(object):
        
        def __init__(self, codNfSerie, numero, serie, numero_nf, dataEmissao_nf, valorNota, chaveAcesso, qtvol ):
            self.codNfSerie = codNfSerie
            self.numpedcli = numero
            self.numnf = numero_nf
            self.serienf = serie
            #self.dteminf = date.fromisoformat((nota['dataEmissao'])[0:10]).strftime('%d-%m-%Y')
            self.dteminf = dataEmissao_nf
            self.vltotalnf = valorNota
            self.qtvol = qtvol
            self.chavenf =chaveAcesso
            #self.cgc_transp = "".join(re.findall("\d+","00.000.000/0000-00"))
            #self.uf_trp = "ES"
            self.status =  1

        @classmethod
        def from_json(cls, json_string):
            json_dict = json.loads(json_string)
            return cls(**json_dict)

        def __repr__(self):
            return f'<sku {self.numpedcli}>'     


        
    class ItensNF(object):
        #def __init__(self, desconto, observacoes, observacaointerna, data, numero, numeroOrdemCompra, vendedor, valorfrete, totalprodutos, totalvenda, situacao, dataSaida, loja, numeroPedidoLoja, tipoIntegracao, cliente, nota  , transporte, itens, parcelas):
        def __init__(self, numseq, codigo, quantidade, vlr_unit):
            self.numseq = numseq
            self.codprod = codigo
            self.qtprod = quantidade
            self.vlr_unit = vlr_unit

            #price = "14000,45"
            #price_in_decimal = Decimal(price.replace(',','.'))



            
        @classmethod
        def from_json(cls, json_string):
            json_dict = json.loads(json_string)
            return cls(**json_dict)

        def __repr__(self):
            return f'<codigo do produto {self.codprod}>' 


    # checar aqui se a lista de numero de pedido tem algum registo no Model do Django pdd_ittset (Linha 45)
   
    dd_numPed_acumulado = []
    for o in dados['retorno']['pedidos']:
        dd = o['pedido']
        dd_numPed_acumulado.append(dd['numero'])
        

    pedd_bling_num = set(dd_numPed_acumulado)

    print("--- pedd_bling_num ---->", pedd_bling_num)
       
    conj = (pedd_bling_num - pdd_ittset)  # Um conjunto de pedidos do bling (-) conjunto de pdd db itotal)
   
    #dd_pedido_acumulado = []
    for u in dados['retorno']['pedidos']:
        dd_pedido ={}

        i = json.dumps(u['pedido'])
        j = u['pedido']
        pedido = u['pedido']

        #print("i ----->", pedido)
        print("****  Print numero Pedido ******" , pedido['numero'])

        if '"nota":' not in i:
            continue
            
        if j['numero'] in conj:
            #print("---- existe u[numero] ---", j['numero']) 
            print("---- tem registro para incluir ")
            

        else:
            print("---- NÃO tem registro para inclui ---")
            continue
    
        if "numeroPedidoLoja" in pedido:
            print("O dicionário possui a chave")
            print("sim")
            print(pedido['numeroPedidoLoja'])
            print(" COM numero Pedido na Loja ", pedido['numeroPedidoLoja'])
        else:
            print("O dicionário NÃO possui a chave")
            print("não")
            #print(pedido['numeroPedidoLoja'])
            pedido['numeroPedidoLoja'] = ""
            print(" SEM numero Pedido na Loja ################################>>>>>")

        #exit(99)

        # checar aqui se a lista de numero de pedido tem algum registo no Model do Django pdd_ittset (Linha 45)

        #pedido = u['pedido']
        #dd_pedido['data'] = pedido['data']
        dd_pedido['numero'] = pedido['numero']
        #dd_pedido['vendedor'] = pedido['vendedor']
        #dd_pedido['totalvenda'] = pedido['totalvenda']
        #dd_pedido['situacao'] = pedido['situacao']
        #dd_pedido['dataSaida'] = pedido['dataSaida']
        #dd_pedido['numeroPedidoLoja'] = pedido['numeroPedidoLoja']
        

        # nota
        
       
        nota = u['pedido']['nota']

        """
        if nota['numero'] != '128117':
            #print("--- Nota Numero ------>", nota['numero'])
            continue
        """
        


        dd_pedido['codNfSerie'] = nota['numero'] + "-" + nota['serie']
        dd_pedido['serie'] = nota['serie']
        dd_pedido['numero_nf'] = nota['numero']
        dd_pedido['dataEmissao_nf'] = nota['dataEmissao']
        dd_pedido['valorNota'] = nota['valorNota']
        dd_pedido['chaveAcesso'] = nota['chaveAcesso']

        #dd_pedido_acumulado.append(dd_pedido)

        
        #print('-- dd_pedido ----->', json.dumps(dd_pedido))
        
        # for para localizar os itens e salvar
        dd_item_acumulado = []

        qt_vol = 0
        z = 1
        for j in u['pedido']['itens']:

            c_item =  j['item']
            dd_item = {}
            dd_item['numseq'] = z
            dd_item['codigo'] = c_item['codigo'] if c_item['codigo'].find('-') < 0 else c_item['codigo'][:c_item['codigo'].find('-')]
            dd_item['quantidade'] = c_item['quantidade']
            dd_item['vlr_unit'] = c_item['valorunidade'][:c_item['valorunidade'].find(".")+3]

            qt_vol = qt_vol + int(Decimal(c_item['quantidade']))
            #qt_vol = qt_vol + int(c_item['quantidade'])
            z = z + 1
            


            #Decimal(valorunidade.replace(',','.'))
        
            #print("valor dd_item['vlr_unit']---->", dd_item['vlr_unit'])
            #print("valor dd_item['vlr_unit']---->", c_item['valorunidade'])


            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            

            #c =  json.dumps(j['item'])

            dd_pedido['qtvol'] = qt_vol

            print("dd_pedido==hoje====>>>", dd_pedido)
            #exit(99)

            its = ItensNF.from_json(json.dumps(dd_item))

            jsonStrIts = json.dumps(its.__dict__)
            
            JsonDictIts = json.loads(jsonStrIts)

            dd_item_acumulado.append(JsonDictIts)
            

            #print("-----------------JsonDictIts--------------", JsonDictIts)
            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
        
        #pedd = Pedidos.from_json(i)
        pedd = NotaFiscalSaida.from_json(json.dumps(dd_pedido))

        #its = Itens.from_json(i)

        jsonStr = json.dumps(pedd.__dict__)

        #jsonStrIts = json.dumps(its.__dict__)


        jsonDict = json.loads(jsonStr)

        #JsonDictIts = json.loads(jsonStrIts)

        myDict3 = {}
        myDict3["itens"] = dd_item_acumulado

        #print("mmmmmmmm myDict3 mmmmmmmmm", myDict3)


        jsonDict.update(myDict3)

        #print("############## jsonDict ###############" , json.dumps(jsonDict))

        #exit(6)
        
        resultado_retorno = testarPost.AddBasePedidos(jsonDict, db)

        #print("#######  resultado_retorno ########", resultado_retorno)

    n = n+1






