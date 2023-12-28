import json, requests, urllib
import os
from dotenv import load_dotenv
from datetime import date
import datetime
import base64
from base64 import b64encode

#import pickle

from pedidos.models import NotasFiscaisSaida


# incluído para testar, porque cnpj da f3c estava dando erro.
#cnpj_temporario = "35457333000129"


# está recebendo um json
def pddNotaFiscalPost(dados):

    print("--- nome do arquivo pdf ---->",  dados['danfefilename'])
    print(type(dados['danfefilename']))
    #   "pdf/" + 


    #exit(22)

     
    with open( "pdf/" + dados['danfefilename'] , "rb") as pdf_file:
        base64_bytes = base64.b64encode(pdf_file.read())
        #print(base64_bytes)
        stringData = base64_bytes.decode('utf8')
        #print(stringData)
    

    
    
    
    #print(encoded_string)
    
    

    #exit(22)
    
    # dados nf ----------------------------------------------------
    newDadosNf = {}
    #newDadosNf['CGCCLIWMS'] = cnpj_temporario  # correto---> str(dados['cgccliwms'])
    newDadosNf['CGCCLIWMS'] = str(dados['cgccliwms'])
    newDadosNf['CGCEMINF'] = str(dados['cgceminf'])
    newDadosNf['NUMPEDCLI'] = dados['numpedcli']

    newDadosNf['NUMNF'] = str(dados['numnf'])
    newDadosNf['SERIENF'] = dados['serienf']
    newDadosNf['DTEMINF'] = date.fromisoformat((dados['dteminf'])[0:10]).strftime('%d/%m/%Y')
    newDadosNf['VLTOTALNF'] = dados['vltotalnf']
    newDadosNf['QTVOL'] = str(dados['qtvol'])

    newDadosNf['CHAVENF'] = dados['chavenf']
    #newDadosNf['CHAVENF'] = base64.b64encode(dados['chavenf'].encode('ascii')).decode('ascii')

    #newDadosNf['situacao'] = dados['situacao']
    newDadosNf['DANFEFILENAME'] = dados['danfefilename']
    newDadosNf['DANFEFILESIZE'] = dados['danfefilesize']
    newDadosNf['DANFEPDFBASE64'] = stringData

    newDadosNf['CGCTRANSP'] = dados['cgc_transp'] if dados['cgc_transp'] != None else ""

    #newDadosNf['xmlNf'] = dados['xmlNf']
    #newDadosNf['linkDanfe'] = dados['linkDanfe']




    
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


    #exit(78)
    #myDict3 = {}
    #myDict3['ITENS'] = (acumItens)
    #jsonDict.update(myDict3)

     
    myDict1 = {}
    myDict1['CORPEM_ERP_CONF_NF'] = newDadosNf

    #print(myDict1)
    #print("fim pedidos Post")

    #exit(67)

    return myDict1





#######################################################################################################
    
def pddNotaFiscalPostEnviar(dados):

    #print(" dados Fase 2 pedidosPostEnviar ---->", dados)
    #print(type(dados))

    #with open('uploadnf/log/' + "Fornecedor", 'a' , encoding="utf-8") as f:
        #f.write(json.dumps(response.text))
        #f.write(response.text)
        #f.write(dados)
    #    f.write(json.dumps(dados))



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
    
    teste = dados['CORPEM_ERP_CONF_NF']
    #print(teste['NUMNF']) NUMPEDCLI

    numnf = teste['NUMNF']
    numpedcli = teste['NUMPEDCLI']

    dados_json = json.dumps(dados, ensure_ascii=False)
   
    #print("dados_json------ antes de enviar ---->", dados_json)


    with open('uploadnf/log/arquivo_dados_Nfe-Pdd_nr' + numpedcli   +   '.txt','a') as f:
        f.write(str(dados_json))



    #payload = dados
    #print("----- print(payload ***-*) ------>>", payload)
    
    #url = "http://serrapark.dd.spiritlinux.com:81/scripts/mh.dll/wc"
    #1 url = "http://10.168.254.1:81/scripts/mh.dll/wc"
    url = "http://10.168.254.1/scripts/mh.dll/wc"


    #payload = "{\"CORPEM_ERP_MERC\": {\"CGCCLIWMS\": \"38317322000131\", \"PRODUTOS\": [{\"CODPROD\": \"11106\", \"NOMEPROD\": \"IMPRESSORA EPSON MATRICIAL FX890 BLACK - C11C524142\", \"TPOLRET\": \"0\", \"IWS_ERP\": \"0\", \"IAUTODTVE\": \"0\", \"QTDDPZOVEN\": \"0\", \"ILOTFAB\": \"0\", \"IDTFAB\": \"0\", \"IDTVEN\": \"0\", \"INSER\": \"1\", \"CODFAB\": \"L117079B\", \"NOMEFAB\": \"\", \"ITENS\": [{\"CODUNID\": \"FR\", \"FATOR\": \"1\", \"CODBARRA\": \"010343913981\", \"PESOLIQ\": \"0.000\", \"PESOBRU\": \"14.000\", \"ALT\": \"18\", \"LAR\": \"44\", \"COMP\": \"36\", \"VOL\": 1}]}]}}"
    headers = {
        'content-type': "application/json; charset=utf-8",
        'cache-control': "no-cache",
        'postman-token': "bd816b6d-e4b5-957b-0028-c47e2ae27fdf"
        }

    ## Acertar aqui com try (tentar acessar o servidor e aguardar resposta, para ver se dá erro, se der erro o que fazer ?)
    response = requests.request("POST", url, data=dados_json, headers=headers)

    # code
    """
    print("Testar conecção com SerraPark")
    try:
        #r = requests.get(url, timeout=1, verify=True)
        response = requests.request("POST", url, data=dados_json, headers=headers, timeout=60, verify=True)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error")
        print(errh.args[0])
    except requests.exceptions.ReadTimeout as errrt:
        print("Time out")
    except requests.exceptions.ConnectionError as conerr:
        print("Connection error")
    except requests.exceptions.RequestException as errex:
        print("Exception request")

    """

    #print(response.text.encode('utf-8'))


    if response.status_code == 200:
        #print(" Achou a Pagina retorno 200 ========>)")
        #print(response.text.encode('utf-8'))
        #print(response.json())
        #print()
        if ("CORPEM_WS_OK" in response.text):
          
            print("******* Sucess *******")
            #print()
            pdd =NotasFiscaisSaida.objects.get(numpedcli = numpedcli)
            pdd.status = 3
            pdd.save()
        else:
            print("#### erro ####",response.text.encode('utf-8'))
            pdd =NotasFiscaisSaida.objects.get(numpedcli = numpedcli)
            pdd.rejeicao = response.text
            pdd.save()
            print()


    filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    #print("----filename1----", filename1)
    filename2 = 'NotaFiscal-'+ numnf + '-' +filename1+'.json'
    #print("----filename2----", filename2)


    with open('uploadnf/log/' + filename2, 'a' , encoding="utf-8") as f:
        #f.write(json.dumps(response.text))
        f.write(response.text)
        f.write(dados_json)
        
        print("salvou....")
        
        print("salvou....")


    
    print('passou por aqui..')
       
    return response
   
