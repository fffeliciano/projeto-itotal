import os, sys
#testando git
#Funcionou corretamente
projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

#exit(90)



#import json 
from uploadnf.pedido import testarPost
from uploadnf.pedido.itotal import con_ittPedidosNew
import re
import json, requests, urllib

from dotenv import load_dotenv
import time
from datetime import datetime, timedelta, date
from decimal import Decimal

import logging

logger = logging.getLogger(__name__)

logger.info("teste de passagem importarPedidos - 0")


# vou comentar esta linha



#----------------------------------------------

load_dotenv()
BLING_SECRET_KEY = os.getenv("BLING_API_KEY")

#N = 90

# n numero de dias atras.
n = 2


x = datetime.now()

#print("valor de x ", x)
#print("--- weekday ==> ", x.weekday())
#date_N_days_ago = datetime.now() - timedelta(days=3)
#print( " - - new date - - ",date_N_days_ago )
#print("- dia da semana na segunda-feira :", date_N_days_ago.weekday())


if x.weekday() == 0:
    #print(" data inicio nova :", date_N_days_ago - timedelta(days=3))
    n = 5
elif int(x.strftime("%H")) > 14:
    n = 2
else:
    #print("data normal")
    n = 2


#if int(x.strftime("%H")) > 10:
#    n = 0
#else:
#    n = 1

#print("---n = a : ", n)

#exit(99)

#date_N_days_ago = datetime.now() - timedelta(days=n)
date_N_days_ago = datetime.now() - timedelta(hours=240)
#timedelta(hours=24)


#date_inicio_formated = date_N_days_ago.strftime("%d/%m/%Y")
date_inicio_formated = date_N_days_ago.strftime("%d/%m/%Y %H:%M:%S")
"%m/%d/%Y, %H:%M:%S"


#print(date_inicio_formated)
#print()
#date_fim_formated = datetime.now().strftime("%d/%m/%Y") 
date_fim_formated = datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
#print(date_fim_formated)
#print()
# data inicio para pesquisa no django drf 
date_inicio_itt = date_N_days_ago.strftime("%Y-%m-%d")


#periodo = []
periodo1 = date_inicio_formated
periodo2 = date_fim_formated


#--------------------------------------------------------------------- excluir/comentar estas linhas
#periodo1 = "01/12/2023"
#periodo2 = "17/12/2023"
#---------------------------------------------------------------- excluir/comentar estas linhas

print("--Periodo1", periodo1)
print("--Periodo2", periodo2)


#exit(97)


db = "/pedidos/pedidos/"

retorno_djg = con_ittPedidosNew(page='all')


print("retorno do django ====>", retorno_djg)
pdd_ittset = set(retorno_djg)
print("pdd_itt--->", pdd_ittset)

situacao_id= "9"

n = 1
lista_pdd_bling = []

while True:

    url = f"https://bling.com.br/Api/v2/pedidos/page={n}/json/"


    payload = {
        "apikey": BLING_SECRET_KEY,
        "filters": f"dataAlteracao[{periodo1} TO {periodo2}]; \
        idSituacao[{situacao_id}]",
    }
    print("payload a aplicar :>>>>>>", payload)
    



    try:
        response = requests.get(url, params=payload)

        print(response.status_code)
        
        dados = json.loads(response.content)


        #with open('dados_blind_teste.json', 'a', encoding='utf-8') as f:
        #    f.write(json.dumps(dados, ensure_ascii=False))


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

    with open('arquivo_dados_pedidos_finalizados.json', 'a', encoding='utf-8') as f:
               json.dump(data, f)
               #f.write(str(data))


    #print("data----->", data)

    #exit(99)


    if response == 200:
        continue

    if "erros" in datas:
        print("===== achei erro 14 =====>")
        break


    # -> response = requests.get(url, params=payload)
    # -> dados = json.loads(response.content)

    #print("*** Print Dados ****>>>", dados)

    class Pedidos(object):
        
        def __init__(self, data, numero, vendedor, totalvenda, situacao, dataSaida, numeroPedidoLoja, nome, cnpj, endereco, numero_end, bairro, complemento, cidade, cep, uf, email, celular, serie, numero_nf, dataEmissao_nf, valorNota, chaveAcesso, qtvol, cgc_transp, codigo_rastreamento, ect_tpserv, ie, cod_carga, integracao, loja ):
            self.obsped = ""
            self.obsrom = ""
            self.numpedcli = numero
            self.numpedrca = numeroPedidoLoja
            self.vltotped = totalvenda
            self.ect_tpserv = ""                #ect_tpserv
            self.cgcdest = "".join(re.findall("\d+", cnpj))
            self.iedest = ""                    #ie
            self.nomedest = nome[:100]
            self.cepdest = "".join(re.findall("\d+", cep))
            self.ufdest = uf
            self.ibgemundest = ""
            self.mun_dest = cidade
            self.bair_dest = bairro
            self.logr_dest = endereco
            self.num_dest = numero_end[:6]
            #self.comp_dest = complemento[0:49].encode('utf-8')
            self.comp_dest = complemento[0:49].replace("’","")
            self.tp_frete = "C"
            self.codvendedor = ""
            self.nomevendedor = vendedor
            #self.dtinclusaoerp = date.fromisoformat(data).strftime('%d-%m-%Y')
            self.dtinclusaoerp = data

            #self.dtliberacaoerp = date.fromisoformat(dataSaida).strftime('%d-%m-%Y')
            self.dtliberacaoerp = dataSaida

            #self.dtprev_ent_site = date.fromisoformat(data).strftime('%d-%m-%Y')
            self.dtprev_ent_site = data

            self.situacao = situacao
            self.emailrastro = email
            self.dddrastro = ""
            self.telrastro = ""
            self.numnf = numero_nf
            self.serienf = serie
            #self.dteminf = date.fromisoformat((nota['dataEmissao'])[0:10]).strftime('%d-%m-%Y')
            self.dteminf = dataEmissao_nf
            self.vltotalnf = valorNota
            self.qtvol = qtvol
            self.chavenf =chaveAcesso
            #self.cgc_transp = "".join(re.findall("\d+","00.000.000/0000-00")) 
            self.cgc_transp = cgc_transp
            self.uf_trp = "ES"
            self.status =  1
            self.cod_carga = cod_carga
            self.codigo_rastreamento = codigo_rastreamento
            self.integracao = integracao
            #self.loja = loja
            #self.loja = numeroPedidoLoja[:numeroPedidoLoja.find('-')] if integracao == 'SkyHub' else integracao
            self.loja = numeroPedidoLoja[:numeroPedidoLoja.find('-')] if integracao == 'SkyHub' else 'Magalu' if integracao == 'IntegraCommerce' else integracao



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
    for o in dados['retorno']['pedidos']:
        dd = o['pedido']
        dd_numPed_acumulado.append(dd['numero'])
        

    pedd_bling_num = set(dd_numPed_acumulado)
       
    conj = (pedd_bling_num-pdd_ittset)
   
    #dd_pedido_acumulado = []
    for u in dados['retorno']['pedidos']:
        dd_pedido ={}

        i = json.dumps(u['pedido'])
        j = u['pedido']
        #t = j['transporte']
        pedido = u['pedido']

        #print("------- transporte -------", t)
        #print("------- pedido -----------" , u)

        #print("i ----->", pedido)
        #print("****  Print i ******" , pedido['numero'])
        

        #exit(99)

        """if '"nota":' not in i:
            continue"""




        if j['numero'] in conj:
            #print("---- existe u[numero] ---", j['numero']) 
            print("---- tem registro para incluir ")
            

        else:
            print("---- não existe ---")
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
        dd_pedido['data'] = pedido['data']
        dd_pedido['numero'] = pedido['numero']
        dd_pedido['vendedor'] = pedido['vendedor']
        dd_pedido['totalvenda'] = pedido['totalvenda']
        dd_pedido['situacao'] = pedido['situacao']
        dd_pedido['dataSaida'] = pedido['dataSaida']
        dd_pedido['numeroPedidoLoja'] = pedido['numeroPedidoLoja']
                
        # cliente
        cliente = u['pedido']['cliente']
        dd_pedido['nome'] = cliente['nome']
        dd_pedido['cnpj'] = cliente['cnpj']
        dd_pedido['ie'] = cliente['ie']
        dd_pedido['endereco'] = cliente['endereco']
        dd_pedido['numero_end'] = cliente['numero']
        dd_pedido['bairro'] = cliente['bairro']
        #dd_pedido['complemento'] = cliente['complemento'].encode('utf-8')
        dd_pedido['complemento'] = cliente['complemento']
        dd_pedido['cidade'] = cliente['cidade']
        dd_pedido['cep'] = cliente['cep']
        dd_pedido['uf'] = cliente['uf']
        dd_pedido['email'] = cliente['email']
        dd_pedido['celular'] = cliente['celular']

        # nota
        """nota = u['pedido']['nota']
        dd_pedido['serie'] = nota['serie']
        dd_pedido['numero_nf'] = nota['numero']
        dd_pedido['dataEmissao_nf'] = nota['dataEmissao']
        dd_pedido['valorNota'] = nota['valorNota']
        dd_pedido['chaveAcesso'] = nota['chaveAcesso']"""

        if 'nota' in pedido:
            nota = u['pedido']['nota']
            dd_pedido['serie'] = nota['serie']
            dd_pedido['numero_nf'] = nota['numero']
            dd_pedido['dataEmissao_nf'] = nota['dataEmissao']
            dd_pedido['valorNota'] = nota['valorNota']
            dd_pedido['chaveAcesso'] = nota['chaveAcesso']
        else:
            nota = "sem conteudo"
            dd_pedido['serie'] = None
            dd_pedido['numero_nf'] = None
            dd_pedido['dataEmissao_nf'] = None
            dd_pedido['valorNota'] = None
            dd_pedido['chaveAcesso'] = None

        
        if 'codigosRastreamento' in pedido:
            rastreamento = u['pedido']['codigosRastreamento']
            result_rastreamento = rastreamento['codigoRastreamento']
        else:
            result_rastreamento = None

        dd_pedido['codigo_rastreamento'] = result_rastreamento
        dd_pedido['ect_tpserv'] = ""
        dd_pedido['cod_carga'] = result_rastreamento
        #dd_pedido['integracao'] = pedido['tipoIntegracao']

        if 'tipoIntegracao' in pedido:
            dd_pedido['integracao'] = pedido['tipoIntegracao']
        else:
            dd_pedido['integracao'] = "Venda Direta"
        

        if 'loja' in pedido:
            dd_pedido['loja'] = pedido['loja']
        else:
            dd_pedido['loja'] = "Ipiranga"

        #dd_pedido['loja'] = pedido['loja']
        
        
        if 'transporte' in pedido:
            tsp = u['pedido']['transporte']
            if 'cnpj' in tsp:
                result_transp = tsp['cnpj']
            else:
                result_transp = "".join(re.findall("\d+","00.000.000/0000-00"))
        else:
            result_transp = "".join(re.findall("\d+","00.000.000/0000-00"))
        

        dd_pedido['cgc_transp'] = result_transp

        #print("cnpj transportadora :", dd_pedido['cgc_transp'])
        

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
            z = z + 1
            
            #Decimal(valorunidade.replace(',','.'))
        
            #print("valor dd_item['vlr_unit']---->", dd_item['vlr_unit'])
            #print("valor dd_item['vlr_unit']---->", c_item['valorunidade'])


            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            

            #c =  json.dumps(j['item'])

            dd_pedido['qtvol'] = qt_vol

            its = Itens.from_json(json.dumps(dd_item))

            jsonStrIts = json.dumps(its.__dict__)
            
            JsonDictIts = json.loads(jsonStrIts)

            dd_item_acumulado.append(JsonDictIts)
            

            #print("-----------------JsonDictIts--------------", JsonDictIts)
            #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
        
        #pedd = Pedidos.from_json(i)
        pedd = Pedidos.from_json(json.dumps(dd_pedido))

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
        #continue
        
        print("cheguei até aqui -*******")
        #exit(6)
        resultado_retorno = testarPost.AddBasePedidos(jsonDict, db)
        #resultado_retorno = testarPost.AddBasePAddBasePedidosedidos(jsonDict)

        print("#######  resultado_retorno ########", resultado_retorno)
        print("vou quebrar aqui!!!")
        #exit(90)
    n = n+1


