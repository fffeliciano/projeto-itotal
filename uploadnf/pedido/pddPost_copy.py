import os, sys

projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','inventario.settings')
django.setup()


import json, requests, urllib
import os
from dotenv import load_dotenv
from datetime import date
import datetime
import re
import logging
import base64
from base64 import b64encode



from pedidos.models import Pedidos, Itens

from base64 import b64encode

logger = logging.getLogger(__name__)


# incluído para testar, porque cnpj da f3c estava dando erro.
#cnpj_temporario = "35457333000129"

r = re.compile(r'\D')


# está recebendo um json
def pedidoPost(dados):


    #--- Etiqueta -----------------------------------------------------

    newEtq = "zero"
    #logger.info(dados['numnf'])
    #logger.info(type(dados['numnf']))
    #logger.info(type(str(dados['numnf'])))
    #logger.info(dados['numpedrca'])
    #logger.info(type(dados['numpedrca']))
    #logger.info(type(str(dados['numpedrca'])))
    nr_tamanho = 0


    """
    try:
        with open( "etiquetas/" + str(dados['numnf']) +".pdf"  , "rb" ) as pdf_file:
            base64_bytes = base64.b64encode(pdf_file.read())
            logger.info("Achei arquivo, e converti em base64")
    
            newEtq = base64_bytes.decode('utf8')
            logger.info("valor de newEtq : {b}".format(b=newEtq))
    
    except FileNotFoundError:
    
            logger.exception("Sorry, file not exist!!")

            msg = "*** Sorry, the file does not exist."
            logger.warning(msg)

#            exit(90)

    logger.info("Situação do programa, passou pelo try, sem problemas")

    #exit(65)
    """

    #--- Etiqueta -----------------------------------------------------
    # Aqui, verificar se o pedido é envvias ou b2w continua como está
    # Se for Shopee temos que pegar o numero do pedido na Shopee aqui!!
    #
    # ver campo que tem o nemro do pedido na Shopee
    #
    # criar um if para pesquisar numero de nf ou nr de pedido shopee. 


    try:
        with open( "etiquetas/" + str(dados['numnf']) +".zpl"  , "rb" ) as zpl_file:
            base64_bytes = base64.b64encode(zpl_file.read())

            newEtq = base64_bytes.decode('utf8')
            #print(newEtq)
            #exit(90)

        try:
            with open ( "etiquetas/" + str(dados['numnf']) +".txt", "r" ) as nr:
                nr_tamanho = nr.read()

                #print("--- nr_tamanho --->", nr_tamanho)
        except FileNotFoundError:
           logger.warning("Arquivo não encontrado")

    except FileNotFoundError:
        logger.warning("*** Sorry, the file does not exist.")


    #logger.info("Situação do programa, passou pelo try, sem problemas")



    #--- Etiqueta fim -------------------------------------------------


    # dados nf ----------------------------------------------------
    newDadosNf = {}
    #newDadosNf['CGCCLIWMS'] = cnpj_temporario  # correto---> str(dados['cgccliwms'])
    newDadosNf['CGCCLIWMS'] = str(dados['cgccliwms'])
    newDadosNf['CGCEMINF'] = str(dados['cgceminf'])
    newDadosNf['OBSPED'] = dados['obsped']
    newDadosNf['OBSROM'] = dados['obsrom']
    newDadosNf['NUMPEDCLI'] = dados['numpedcli']
    newDadosNf['NUMPEDRCA'] = r.sub('', dados['numpedrca'])
    newDadosNf['VLTOTPED'] = dados['vltotped']
    newDadosNf['CGCDEST'] = dados['cgcdest']
    newDadosNf['NOMEDEST'] = dados['nomedest']
    newDadosNf['CEPDEST'] = dados['cepdest']
    newDadosNf['UFDEST'] = dados['ufdest']
    newDadosNf['IBGEMUNDEST'] = dados['ibgemundest']
    newDadosNf['MUN_DEST'] = dados['mun_dest']
    newDadosNf['BAIR_DEST'] = dados['bair_dest']
    newDadosNf['LOGR_DEST'] = dados['logr_dest']
    newDadosNf['NUM_DEST'] = dados['num_dest']
    newDadosNf['COMP_DEST'] = dados['comp_dest']
    newDadosNf['TP_FRETE'] = dados['tp_frete']
    newDadosNf['CODVENDEDOR'] = dados['codvendedor']
    newDadosNf['NOMEVENDEDOR'] = dados['nomevendedor']

    newdata0 = datetime.datetime.strptime((dados['dtinclusaoerp']), '%Y-%m-%d')
    newDadosNf['DTINCLUSAOERP'] = datetime.datetime.strftime(newdata0, format('%d-%m-%Y'))

    newdata1 = datetime.datetime.strptime((dados['dtinclusaoerp']), '%Y-%m-%d')
    newDadosNf['DTLIBERACAOERP'] = datetime.datetime.strftime(newdata1, format('%d-%m-%Y'))

    newdata2 = datetime.datetime.strptime((dados['dtinclusaoerp']), '%Y-%m-%d')
    newDadosNf['DTPREV_ENT_SITE'] = datetime.datetime.strftime(newdata2, format('%d-%m-%Y'))
    
    newDadosNf['EMAILRASTRO'] = dados['emailrastro']
    newDadosNf['DDDRASTRO'] = dados['dddrastro']
    newDadosNf['TELRASTRO'] = dados['telrastro']

    #newDadosNf['NUMNF'] = str(dados['numnf'])
    #newDadosNf['SERIENF'] = dados['serienf']
    #newDadosNf['DTEMINF'] = date.fromisoformat((dados['dteminf'])[0:10]).strftime('%d-%m-%Y')
    #newDadosNf['VLTOTALNF'] = dados['vltotalnf']
    #newDadosNf['QTVOL'] = str(dados['qtvol'])
    #newDadosNf['CHAVENF'] = dados['chavenf']

    newDadosNf['CGC_TRP'] = dados['cgc_transp']
    newDadosNf['UF_TRP'] = dados['uf_trp']
    newDadosNf['PRIORIDADE'] = "ALTA"  
    newDadosNf['ETQCLIFILESIZE'] = nr_tamanho
    newDadosNf['ETQCLIZPLBASE64'] = newEtq
    
    # itens --------------------------------------------------------
    acumItens = []
    for n in dados['itens']:
        dados_list = {}
        dados_list['NUMSEQ'] = str(n['numseq'])
        dados_list['CODPROD'] = str(n['codprod'])
        dados_list['QTPROD'] = str(n['qtprod'])
        #dados_list['VLTOTPROD'] = n['vlr_unit']
        acumItens.append(dados_list)


    newDadosNf['ITENS'] = acumItens

    #print("newDadosNf--->", newDadosNf)
    #print("acumItens--->",acumItens)

    #logger.warning("Segue o valor do json newDadosNf --> {a}".format(a=newDadosNf))

#    with open('uploadnf/log/arquivo_dados_nf" + str()   +   ".txt','a') as f:
#        f.write(str(newDadosNf))






    #exit(78)
    #myDict3 = {}
    #myDict3['ITENS'] = (acumItens)
    #jsonDict.update(myDict3)

     
    myDict1 = {}
    myDict1['CORPEM_ERP_DOC_SAI'] = newDadosNf

    print(myDict1)
    print("fim pedidos Post")

    #exit(67)

    return myDict1





#######################################################################################################
    
def pedidoPostEnviar(dados):

    print(" dados Fase 2 pedidosPostEnviar ---->", dados)
    print(type(dados))

    #exit(5)

    # Início Fase 2
    # Salvar dados de Produtos na CORPEM_ERP  

    #json_dados = '''{"CORPEM_ERP_MERC": {"CGCCLIWMS": "38317322000131", "PRODUTOS": [{"CODPROD": "36692", "NOMEPROD": "APARADOR PHILIPS ONE BLADE QP2510/10", "TPOLRET": "0", "IWS_ERP": "0", "IAUTODTVE": "0", "QTDDPZOVEN": "0", "ILOTFAB": "0", "IDTFAB": "0", "IDTVEN": "0", "INSER": "1", "CODFAB": "19807", "NOMEFAB": "", "ITENS": [{"CODUNID": "FR", "FATOR": "1", "CODBARRA": "8710103821359", "PESOLIQ": "0.00000", "PESOBRU": "0.00000", "ALT": "", "LAR": "", "COMP": "", "VOL": ""}]}]}}'''
    #json_dados = '''{"CORPEM_ERP_MERC": {"CGCCLIWMS": "38317322000131", "PRODUTOS": [{"CODPROD": "36692", "NOMEPROD": "APARADOR PHILIPS ONE BLADE QP2510/10", "TPOLRET": "0", "IWS_ERP": "0", "IAUTODTVE": "0", "QTDDPZOVEN": "0", "ILOTFAB": "0", "IDTFAB": "0", "IDTVEN": "0", "INSER": "1", "CODFAB": "19807", "NOMEFAB": "", "ITENS": []}]}}'''

    


    


    
    
    #print("-------|codprod|---------", dados.codprod)

    # 38317322000131

    #dados_json = dados
    #dados_json = json.dumps(dados)



    #print("dados_json_dumps", dados_json)

    #exit(7)
    
    teste = dados['CORPEM_ERP_DOC_SAI']
    #print(teste['NUMNF']) NUMPEDCLI
    numpedcli = teste['NUMPEDCLI']

    dados_json = json.dumps(dados, ensure_ascii=False)
   
    #print("dados_json------ antes de enviar ---->", dados_json)


    with open('uploadnf/log/arquivo_dados_nf' + numpedcli   +   '.txt','a') as f:
        f.write(str(dados_json))








    #payload = dados
    #print("----- print(payload ***-*) ------>>", payload)
    
    #url = "http://serrapark.dd.spiritlinux.com:81/scripts/mh.dll/wc"
    #url = "http://10.168.254.1:81/scripts/mh.dll/wc"
    url = "http://10.168.254.1/scripts/mh.dll/wc"


    #payload = "{\"CORPEM_ERP_MERC\": {\"CGCCLIWMS\": \"38317322000131\", \"PRODUTOS\": [{\"CODPROD\": \"11106\", \"NOMEPROD\": \"IMPRESSORA EPSON MATRICIAL FX890 BLACK - C11C524142\", \"TPOLRET\": \"0\", \"IWS_ERP\": \"0\", \"IAUTODTVE\": \"0\", \"QTDDPZOVEN\": \"0\", \"ILOTFAB\": \"0\", \"IDTFAB\": \"0\", \"IDTVEN\": \"0\", \"INSER\": \"1\", \"CODFAB\": \"L117079B\", \"NOMEFAB\": \"\", \"ITENS\": [{\"CODUNID\": \"FR\", \"FATOR\": \"1\", \"CODBARRA\": \"010343913981\", \"PESOLIQ\": \"0.000\", \"PESOBRU\": \"14.000\", \"ALT\": \"18\", \"LAR\": \"44\", \"COMP\": \"36\", \"VOL\": 1}]}]}}"
    headers = {
        'content-type': "application/json; charset=utf-8",
        'cache-control': "no-cache",
        'postman-token': "bd816b6d-e4b5-957b-0028-c47e2ae27fdf"
        }

    response = requests.request("POST", url, data=dados_json, headers=headers)

    #print(response.text.encode('utf-8'))

    dd_ret = {}
    if response.status_code == 200:
        #print(" Achou a Pagina retorno 200 ========>)")
        #print(response.text.encode('utf-8'))
        #print(response.json())
        #print()
        if ("CORPEM_WS_OK" in response.text ) and ("COD_REJ_DOC" not in response.text):
            print("******* Sucess *******")
            #print()
            pdd =Pedidos.objects.get(numpedcli = numpedcli)
            pdd.status = 2
            pdd.save()
        else:

            #data[0]['f'] = var
            print("#### erro ####",response.text.encode('utf-8'))
            #print()


    filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    #print("----filename1----", filename1)
    filename2 = 'Pedido-'+ numpedcli + '-' +filename1+'.json'
    #print("----filename2----", filename2)


    with open('uploadnf/log/' + filename2, 'a' , encoding="utf-8") as f:
        #f.write(json.dumps(response.text))
        f.write(response.text)
        
  
        print("salvou msg....")


    
    #print('passou por aqui..')
       
    return response


### Cancelamento #############################################################################################


def cancelarPedidoPost(dados):
    
    # dados nf ----------------------------------------------------
    newDadosNf = {}
    newDadosNf['CGCCLIWMS'] = str(dados['cgccliwms'])
    newDadosNf['NUMPEDCLI'] = dados['numpedcli']

     
    myDict1 = {}
    myDict1['CORPEM_ERP_CANC_PED'] = newDadosNf

    print(myDict1)
    #exit(67)

    return myDict1





###  Cancelamento  ################################################################################################
    
def cancelarPedidoPostEnviar(dados):

    print(" dados Fase 2 pedidosPostEnviar ---->", dados)
    print(type(dados))


    
    teste = dados['CORPEM_ERP_CANC_PED']
    #print(teste['NUMNF']) NUMPEDCLI
    numpedcli = teste['NUMPEDCLI']
    print(numpedcli)


    dados_json = json.dumps(dados, ensure_ascii=False)
   
    print("dados_json------ antes de enviar ---->", dados_json)
    #payload = dados
    #print("----- print(payload ***-*) ------>>", payload)
    
    #url = "http://serrapark.dd.spiritlinux.com:81/scripts/mh.dll/wc"
    url = "http://10.168.254.1/scripts/mh.dll/wc"

    #payload = "{\"CORPEM_ERP_MERC\": {\"CGCCLIWMS\": \"38317322000131\", \"PRODUTOS\": [{\"CODPROD\": \"11106\", \"NOMEPROD\": \"IMPRESSORA EPSON MATRICIAL FX890 BLACK - C11C524142\", \"TPOLRET\": \"0\", \"IWS_ERP\": \"0\", \"IAUTODTVE\": \"0\", \"QTDDPZOVEN\": \"0\", \"ILOTFAB\": \"0\", \"IDTFAB\": \"0\", \"IDTVEN\": \"0\", \"INSER\": \"1\", \"CODFAB\": \"L117079B\", \"NOMEFAB\": \"\", \"ITENS\": [{\"CODUNID\": \"FR\", \"FATOR\": \"1\", \"CODBARRA\": \"010343913981\", \"PESOLIQ\": \"0.000\", \"PESOBRU\": \"14.000\", \"ALT\": \"18\", \"LAR\": \"44\", \"COMP\": \"36\", \"VOL\": 1}]}]}}"
    headers = {
        'content-type': "application/json; charset=utf-8",
        'cache-control': "no-cache",
        'postman-token': "bd816b6d-e4b5-957b-0028-c47e2ae27fdf"
        }

    response = requests.request("POST", url, data=dados_json, headers=headers)

    #print(response.text.encode('utf-8'))


    if response.status_code == 200:
        #print(" Achou a Pagina retorno 200 ========>)")
        #print(response.text.encode('utf-8'))
        #print(response.json())
        #print()
        if "CORPEM_WS_OK" in response.text:
            print("******* Sucess *******")
            #print()
            pdd =Pedidos.objects.get(numpedcli = numpedcli)
            pdd.status = 5
            pdd.save()
        else:
            print("#### erro ####",response.text.encode('utf-8'))
            #print()


    filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    #print("----filename1----", filename1)
    filename2 = 'Pedido-Cancelado'+ numpedcli + '-' +filename1+'.json'
    #print("----filename2----", filename2)


    with open('uploadnf/log/' + filename2, 'a' , encoding="utf-8") as f:
        #f.write(json.dumps(response.text))
        f.write(response.text)
        
        print("salvou....")
        
        print("salvou....")


    
    print('passou por aqui..')
       
    return response

################################################################################################33


variavel = {
"CORPEM_ERP_DOC_SAI": {
    "cgccliwms": 38317322000131,
    "cgceminf": 38317322000131,
    "obsped": "",
    "obsrom": "",
    "numpedcli": "11958",
    "numpedrca": "Lojas_Americanas-296317036401",
    "vltotped": "1980.00",
    "cgcdest": "65876490920",
    "nomedest": "silvio dos santos dovirgnes",
    "cepdest": "87013000",
    "ufdest": "PR",
    "ibgemundest": "",
    "mun_dest": "Maringá",
    "bair_dest": "Zona 01",
    "logr_dest": "Avenida Brasil",
    "num_dest": "4312",
    "comp_dest": "loja 13 - edificio transamerica",
    "tp_frete": "C",
    "codvendedor": "",
    "nomevendedor": "",
    "dtinclusaoerp": "2022-07-26",
    "dtliberacaoerp": "2022-07-26",
    "dtprev_ent_site": "2022-07-26",
    "emailrastro": "65876490920@email.com.br",
    "dddrastro": "",
    "telrastro": "",
    "numnf": 10579,
    "serienf": "1",
    "dteminf": "2022-07-26T08:07:02-03:00",
    "vltotalnf": "1980.00",
    "qtvol": 2,
    "chavenf": "32220738317322000131550010000105791994806751",
    "cgc_transp": "00000000000000",
    "uf_trp": "ES",
    "status": 1,
    "itens": [
        {
            "numseq": "1",
            "codprod": "1076",
            "qtprod": 2,
            "vlr_unit": "1374.00"
        }
    ]
}
}


resulte = pedidoPost(variavel)
