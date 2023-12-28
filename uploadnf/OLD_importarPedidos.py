import json 
import testarPost_2
import re
import json, requests, urllib
import os
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta, date




#----------------------------------------------

load_dotenv()
BLING_SECRET_KEY = os.getenv("BLING_API_KEY")

#N = 90

# n numero de dias atras.
n = 1

date_N_days_ago = datetime.now() - timedelta(days=n)
#date.today()

date_inicio_formated = date_N_days_ago.strftime("%d/%m/%Y")
#print(date_inicio_formated)
#print()
date_fim_formated = datetime.now().strftime("%d/%m/%Y") 
#print(date_fim_formated)
#print()



#periodo = []
periodo1 = date_inicio_formated
periodo2 = date_fim_formated

#periodo1 = "07/03/2021"
#periodo2 = "08/03/2021"

situacao_id= "9"
tipo = 'P'

n = 1
lista_pdd_bling = []
while True:
    url = f"https://bling.com.br/Api/v2/pedidos/page={n}/json/"

    '''payload = {
        "apikey": BLING_SECRET_KEY,
        "filters": f"dataEmissao[{periodo1} TO {periodo2}]",
    }'''

    payload = {
        "apikey": BLING_SECRET_KEY,
        "filters": f"dataAlteracao[{periodo1} TO {periodo2}]; \
        idSituacao[{situacao_id}]",
    }
    

    



    try:
        response = requests.get(url, params=payload)

        print(response.status_code)
        
        dados = json.loads(response.content)
        #with open('dados_blind_teste.json', 'a', encoding='utf-8') as f:
         #   f.write(json.dumps(dados, ensure_ascii=False))






        if response.status_code == 200:
            #dados = json.loads(response.content)
            

            #with open('dados_blind_teste.json', 'a', encoding='utf-8') as f:
            #    f.write(json.dumps(dados, ensure_ascii=False))
            

            #for w in dados['retorno']['pedidos']:
             #   lista_pdd_bling.append(w['pedido']['numero'])

            print("len nr pedidos :" ,len(dados['retorno']['pedidos']))

            print(" n ---->", n)
        
            print('lista_pdd_bling ------>', lista_pdd_bling)

            print("len nr pedidos incluídos lista", len(lista_pdd_bling))
            

        # Dados pedido Model
        

        # jogar esta parte para o final ----------------------------------------
        nrp = len(dados['retorno']['pedidos'])
        print(' nrp------>', nrp)
        if nrp < 100:
            print("menor que 100, vai brecar")
            break
        
        print(" vai somar 1 em n e continuar")
        
        
        n = n+1 # excluir depois do teste
        continue
        exit(1)
        # jogar esta parte para o final ---------------------------------------

        
        


        # provisório para testes - Excluir
        
        # provisório para testes - Excluir 

        
        
        
        #print(response.content)
     




    

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


    exit(7)

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

    class Pedidos(object):
        
        def __init__(self, data, numero, vendedor, totalvenda, situacao, dataSaida, numeroPedidoLoja, nome, cnpj, endereco, numero_end, bairro, complemento, cep, uf, email, celular, serie, numero_nf, dataEmissao_nf, valorNota, chaveAcesso ):
            self.obsped = ""
            self.obsrom = ""
            self.numpedcli = numero
            self.numpedrca = numeroPedidoLoja
            self.vltotped = totalvenda
            self.cgcdest = "".join(re.findall("\d+", cliente['cnpj']))  
            self.nomedest = cliente['nome']
            self.cepdest = "".join(re.findall("\d+",cliente['cep']))
            self.ufdest = cliente['uf']
            self.ibgemundest = ""
            self.mun_dest = cliente['cidade']
            self.bair_dest = cliente['bairro']
            self.logr_dest = cliente['endereco']
            self.num_dest = cliente['numero']
            self.comp_dest = cliente['complemento'][0:49]
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
            self.emailrastro = cliente['email']
            self.dddrastro = ""
            self.telrastro = cliente['celular']
            self.numnf = nota['numero']
            self.serienf = nota['serie']
            #self.dteminf = date.fromisoformat((nota['dataEmissao'])[0:10]).strftime('%d-%m-%Y')
            self.dteminf = nota['dataEmissao']
            self.vltotalnf = nota['valorNota']
            # Consertar QTVOL 
            self.qtvol = 1
            # Consertar QTVOL 
            self.chavenf = nota['chaveAcesso']
            self.cgc_transp = "".join(re.findall("\d+","00.000.000/0000-00"))
            self.uf_trp = "ES"



        @classmethod
        def from_json(cls, json_string):
            json_dict = json.loads(json_string)
            return cls(**json_dict)



        def __repr__(self):
            return f'<sku {self.numpedcli}>'     


        
    class Itens(object):
        #def __init__(self, desconto, observacoes, observacaointerna, data, numero, numeroOrdemCompra, vendedor, valorfrete, totalprodutos, totalvenda, situacao, dataSaida, loja, numeroPedidoLoja, tipoIntegracao, cliente, nota  , transporte, itens, parcelas):
        def __init__(self, codigo, quantidade, vlr_unit):
        #def __init__(self, codigo, quantidade):
            #self.NUMSEQ = 0
            self.codprod = codigo
            self.qtprod = quantidade
            self.vlr_unit = vlr_unit
            
        @classmethod
        def from_json(cls, json_string):
            json_dict = json.loads(json_string)
            return cls(**json_dict)

        def __repr__(self):
            return f'<codigo do produto {self.codprod}>' 




   

    #print("--  aaaa  ---------")

    # itens
    dd_pedido_acumulado = []
    for u in dados['retorno']['pedidos']:
        dd_pedido ={}

        i = json.dumps(u['pedido'])
        #print("****  Print i ******" , i)

        if "nota" not in i:
            #print("break_0")
            continue
            #print("break_1")
        
        #print(" u ---->", json.dumps(u))
        
        # pedido
        pedido = u['pedido']
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
        dd_pedido['endereco'] = cliente['endereco']
        dd_pedido['numero_end'] = cliente['numero']
        dd_pedido['bairro'] = cliente['bairro']
        dd_pedido['complemento'] = cliente['complemento']
        dd_pedido['cep'] = cliente['cep']
        dd_pedido['uf'] = cliente['uf']
        dd_pedido['email'] = cliente['email']
        dd_pedido['celular'] = cliente['celular']

        # nota
        nota = u['pedido']['nota']
        dd_pedido['serie'] = nota['serie']
        dd_pedido['numero_nf'] = nota['numero']
        dd_pedido['dataEmissao_nf'] = nota['dataEmissao']
        dd_pedido['valorNota'] = nota['valorNota']
        dd_pedido['chaveAcesso'] = nota['chaveAcesso']

        dd_pedido_acumulado.append(dd_pedido)

        
        print('-- dd_pedido ----->', json.dumps(dd_pedido))
        
        # for para localizar os itens e salvar
        dd_item_acumulado = []
        
        for j in u['pedido']['itens']:

            c_item =  j['item']
            dd_item = {}
            dd_item['codigo'] = c_item['codigo']
            dd_item['quantidade'] = c_item['quantidade']
            dd_item['vlr_unit'] = c_item['valorunidade']
        
            #print(dd_item)

            c =  json.dumps(j['item'])

            its = Itens.from_json(json.dumps(dd_item))

            jsonStrIts = json.dumps(its.__dict__)
            
            JsonDictIts = json.loads(jsonStrIts)

            z = z + 1

            #print("-----------------JsonDictIts--------------", JsonDictIts)
       
        
        #pedd = Pedidos.from_json(i)
        pedd = Pedidos.from_json(json.dumps(dd_pedido))

        #its = Itens.from_json(i)

        jsonStr = json.dumps(pedd.__dict__)

        #jsonStrIts = json.dumps(its.__dict__)


        jsonDict = json.loads(jsonStr)

        #JsonDictIts = json.loads(jsonStrIts)

        myDict3 = {}
        myDict3["itens"] = [JsonDictIts]

        #print("mmmmmmmm myDict3 mmmmmmmmm", myDict3)


        jsonDict.update(myDict3)

        print("############## jsonDict ###############" , json.dumps(jsonDict))

        #exit(6)
        resultado_retorno = testarPost.AddBasePedidos(jsonDict)

        print("#######  resultado_retorno ########", resultado_retorno)

    n = n+1


print("cheguei nesta parte final")