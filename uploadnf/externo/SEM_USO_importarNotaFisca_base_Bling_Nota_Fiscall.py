import json 
from uploadnf.pedido import testarPost
from uploadnf.pedido.itotal import con_ittPedidos
import re
import json, requests, urllib
import os
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta, date
#from decimal import Decimal




#----------------------------------------------

load_dotenv()
BLING_SECRET_KEY = os.getenv("BLING_API_KEY")

#N = 90

# n numero de dias atras.
n = 18
#h = 16
#mn = 20

x = datetime.now()

# if int(x.strftime("%H")) > 2:
#    n = 0
#else:
#    n = 1



#date_N_days_ago = datetime.now() - timedelta(days=n)
date_N_days_ago = datetime.now() - timedelta(hours=n)
print(date_N_days_ago , datetime.now() , timedelta(hours=n))
#date_N_days_ago = datetime.now() - timedelta(minutes=mn)

#delta = timedelta(
#...     days=50,
#...     seconds=27,
#...     microseconds=10,
#...     milliseconds=29000,
#...     minutes=5,
#...     hours=8,
#...     weeks=2
#... )



#   12/12/2019 14:01:00 TO 05/02/2020

#1 date_inicio_formated = date_N_days_ago.strftime("%d/%m/%Y")
date_inicio_formated = date_N_days_ago.strftime("%d/%m/%Y %H:%M:%S")
print("horario inicial :", date_inicio_formated)
#print()
#1 date_fim_formated = datetime.now().strftime("%d/%m/%Y") 
date_fim_formated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

print("horario final :",date_fim_formated)
#print()

# data inicio para pesquisa no django drf 
#date_inicio_itt = date_N_days_ago.strftime("%Y-%m-%d")

#1 date_inicio_itt = date_N_days_ago.strftime("%d/%m/%Y %H:%M:%S")


#periodo = []
periodo1 = date_inicio_formated
periodo2 = date_fim_formated



#--------------------------------------------------------------------- excluir/comentar estas linhas
#periodo1 = "17/05/2021"
#periodo2 = "17/05/2021"
#--------------------------------------------------------------------- excluir/comentar estas linhas



#1 retorno_djg = con_ittPedidos(date_inicio_itt)


#1 pdd_ittset = set(retorno_djg)
#print("pdd_itt--->", pdd_ittset)

situacao_id= "6" # Aprovada OU 7 = Danfe Emitida
tipo_nf = "S" # S=Saída  E=Entrada

n = 1
lista_pdd_bling = []
while True:
    url = f"https://bling.com.br/Api/v2/notasfiscais/page={n}/json/"

    payload = {
        "apikey": BLING_SECRET_KEY,
        "filters": f"dataEmissao[{periodo1} TO {periodo2}]; \
        situacao[{situacao_id}]; \
        tipo[{tipo_nf}]",
    }
    
    #print("payload---->",   payload)
    



    try:
        response = requests.get(url, params=payload)

        print(response.status_code)

        #exit(99)
        
        dados = json.loads(response.content)

        with open('dados_blind_teste_Nota_Fiscal.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(dados, ensure_ascii=False))


        exit(7)



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

    class NotasFiscaisSaida(object):
        
        def __init__(self, data, numero, vendedor, totalvenda, situacao, dataSaida, numeroPedidoLoja, nome, cnpj, endereco, numero_end, bairro, complemento, cidade, cep, uf, email, celular, serie, numero_nf, dataEmissao_nf, valorNota, chaveAcesso ):
            self.numpedcli = numero
            self.numnf = numero_nf
            self.serienf = serie
            #self.dteminf = date.fromisoformat((nota['dataEmissao'])[0:10]).strftime('%d-%m-%Y')
            self.dteminf = dataEmissao_nf
            self.vltotalnf = valorNota
            # Consertar QTVOL 
  #          self.qtvol = ????????????
            # Consertar QTVOL 
            self.chavenf =chaveAcesso
            self.cgc_transp = "".join(re.findall("\d+","00.000.000/0000-00"))
            self.uf_trp = "ES"
            self.status =  1



        @classmethod
        def from_json(cls, json_string):
            json_dict = json.loads(json_string)
            return cls(**json_dict)



        def __repr__(self):
            return f'<sku {self.numpedcli}>'     


        
    class Itens(object):
        #def __init__(self, desconto, observacoes, observacaointerna, data, numero, numeroOrdemCompra, vendedor, valorfrete, totalprodutos, totalvenda, situacao, dataSaida, loja, numeroPedidoLoja, tipoIntegracao, cliente, nota  , transporte, itens, parcelas):
        def __init__(self, numseq, codigo, quantidade, vlr_unit):
        #def __init__(self, codigo, quantidade):
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
    for o in dados['retorno']['notasfiscais']:
        dd = o['notafiscal']
        dd_numPed_acumulado.append(dd['numero'])
        

    pedd_bling_num = set(dd_numPed_acumulado)
       
    conj = (pedd_bling_num-pdd_ittset)
   
    dd_pedido_acumulado = []
    for u in dados['retorno']['notasfiscais']:
        dd_pedido ={}

        i = json.dumps(u['notafiscal'])
        j = u['notafiscal']
        notafiscal = u['notafiscal']

        #print("i ----->", notafiscal)
        #print("****  Print i ******" , notafiscal['numero'])

        if "nota" not in i:
            continue
            
        if j['numero'] in conj:
            #print("---- existe u[numero] ---", j['numero']) 
            print("---- tem registro para incluir ")
            

        else:
            print("---- não existe ---")
            continue
    
        if "numeroPedidoLoja" in notafiscal:
            print("O dicionário possui a chave")
            print("sim")
            print(notafiscal['numeroPedidoLoja'])
            print(" COM numero Pedido na Loja ", notafiscal['numeroPedidoLoja'])
        else:
            print("O dicionário NÃO possui a chave")
            print("não")
            #print(pedido['numeroPedidoLoja'])
            notafiscal['numeroPedidoLoja'] = ""
            print(" SEM numero Pedido na Loja ################################>>>>>")

        #exit(99)

        # checar aqui se a lista de numero de pedido tem algum registo no Model do Django pdd_ittset (Linha 45)

        #pedido = u['pedido']
        dd_pedido['data'] = notafiscal['data']
        dd_pedido['numero'] = notafiscal['numero']
        dd_pedido['vendedor'] = notafiscal['vendedor']
        dd_pedido['totalvenda'] = notafiscal['totalvenda']
        dd_pedido['situacao'] = notafiscal['situacao']
        dd_pedido['dataSaida'] = notafiscal['dataSaida']
        dd_pedido['numeroPedidoLoja'] = notafiscal['numeroPedidoLoja']
        
        # cliente
        cliente = u['notafiscal']['cliente']
        dd_pedido['nome'] = cliente['nome']
        dd_pedido['cnpj'] = cliente['cnpj']
        dd_pedido['endereco'] = cliente['endereco']
        dd_pedido['numero_end'] = cliente['numero']
        dd_pedido['bairro'] = cliente['bairro']
        dd_pedido['complemento'] = cliente['complemento']
        dd_pedido['cidade'] = cliente['cidade']
        dd_pedido['cep'] = cliente['cep']
        dd_pedido['uf'] = cliente['uf']
        dd_pedido['email'] = cliente['email']
        dd_pedido['celular'] = cliente['celular']

        # nota
        nota = u['notafiscal']['nota']
        dd_pedido['serie'] = nota['serie']
        dd_pedido['numero_nf'] = nota['numero']
        dd_pedido['dataEmissao_nf'] = nota['dataEmissao']
        dd_pedido['valorNota'] = nota['valorNota']
        dd_pedido['chaveAcesso'] = nota['chaveAcesso']

        dd_pedido_acumulado.append(dd_pedido)

        
        #print('-- dd_pedido ----->', json.dumps(dd_pedido))
        
        # for para localizar os itens e salvar
        dd_item_acumulado = []
        z = 1
        for j in u['notafiscal']['itens']:

            c_item =  j['item']
            dd_item = {}
            dd_item['numseq'] = z
            dd_item['codigo'] = c_item['codigo']
            dd_item['quantidade'] = c_item['quantidade']
            dd_item['vlr_unit'] = c_item['valorunidade'][:c_item['valorunidade'].find(".")+3]
            z = z + 1
            
            #Decimal(valorunidade.replace(',','.'))
        
            #print("valor dd_item['vlr_unit']---->", dd_item['vlr_unit'])
            #print("valor dd_item['vlr_unit']---->", c_item['valorunidade'])


            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            

            #c =  json.dumps(j['item'])

            its = Itens.from_json(json.dumps(dd_item))

            jsonStrIts = json.dumps(its.__dict__)
            
            JsonDictIts = json.loads(jsonStrIts)

            dd_item_acumulado.append(JsonDictIts)
            

            #print("-----------------JsonDictIts--------------", JsonDictIts)
            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
        
        #pedd = NotasFiscaisSaida.from_json(i)
        pedd = NotasFiscaisSaida.from_json(json.dumps(dd_pedido))

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
        resultado_retorno = testarPost.AddBasePedidos(jsonDict)

        #print("#######  resultado_retorno ########", resultado_retorno)

    n = n+1


