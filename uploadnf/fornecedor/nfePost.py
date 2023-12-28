import json, requests, urllib
import os
from dotenv import load_dotenv
from datetime import date
import datetime


from fornecedor.models import NotasFiscais, Itens



# está recebendo um json
def notaFiscalPost(dados):
    
    # dados nf ----------------------------------------------------
    newDadosNf = {}
    ### Alterado linha abaixo, para pegar o CNPJ da nf, para evitar erros
    ### Testar ver se está tudo correto.
    newDadosNf['CGCCLIWMS'] = "38317322000131" 
    #newDadosNf['CGCCLIWMS'] = dados['CNPJ_dest']
    # Após os testes alterar o numero do cnpj pelo campo abaixo
    #newDadosNf['CNPJ_dest'] = dados['CNPJ_dest']
    newDadosNf['CGCREM'] = dados['CNPJ_emit']
    newDadosNf['OBSRESDP'] = ""
    newDadosNf['TPDESTNF'] = dados['ws_tpdestnf']
    newDadosNf['DEV'] = dados['ws_dev']
    newDadosNf['NUMNF'] = dados['nNF']
    newDadosNf['SERIENF'] = dados['serie']
    newDadosNf['DTEMINF'] = date.fromisoformat((dados['dhEmi'])[0:10]).strftime('%d-%m-%Y')
    newDadosNf['VLTOTALNF'] = dados['vProd']   # dados['vNF']
    newDadosNf['NUMEPEDCLI'] = dados['nNF']
    newDadosNf['CHAVENF'] = dados['chNFe']

    # itens --------------------------------------------------------
    acumItens = []
    for n in dados['itens']:
        dados_list = {}
        dados_list['NUMSEQ'] = str(n['nItem'])
        dados_list['CODPROD'] = str(n['nsku'])
        dados_list['QTPROD'] = n['qCom']
        dados_list['VLTOTPROD'] = n['vProd']
        acumItens.append(dados_list)

    
    myDict3 = {}
    myDict3['ITENS'] = (acumItens)
    #jsonDict.update(myDict3)

    myDict1 = {}
    myDict1['CORPEM_ERP_DOC_ENT'] = newDadosNf
    
    myDict1.update(myDict3)

    return json.dumps(myDict1)





    
def notaFiscalPostEnviar(dados):
    # Início Fase 2
    # Salvar dados de Produtos na CORPEM_ERP  

    #json_dados = '''{"CORPEM_ERP_MERC": {"CGCCLIWMS": "38317322000131", "PRODUTOS": [{"CODPROD": "36692", "NOMEPROD": "APARADOR PHILIPS ONE BLADE QP2510/10", "TPOLRET": "0", "IWS_ERP": "0", "IAUTODTVE": "0", "QTDDPZOVEN": "0", "ILOTFAB": "0", "IDTFAB": "0", "IDTVEN": "0", "INSER": "1", "CODFAB": "19807", "NOMEFAB": "", "ITENS": [{"CODUNID": "FR", "FATOR": "1", "CODBARRA": "8710103821359", "PESOLIQ": "0.00000", "PESOBRU": "0.00000", "ALT": "", "LAR": "", "COMP": "", "VOL": ""}]}]}}'''
    #json_dados = '''{"CORPEM_ERP_MERC": {"CGCCLIWMS": "38317322000131", "PRODUTOS": [{"CODPROD": "36692", "NOMEPROD": "APARADOR PHILIPS ONE BLADE QP2510/10", "TPOLRET": "0", "IWS_ERP": "0", "IAUTODTVE": "0", "QTDDPZOVEN": "0", "ILOTFAB": "0", "IDTFAB": "0", "IDTVEN": "0", "INSER": "1", "CODFAB": "19807", "NOMEFAB": "", "ITENS": []}]}}'''

    print(" dados Fase 2 notaFiscalPostEnviar ---->", dados)


    payload = dados

    #print("----- print(payload ***-*) ------>>", payload)
    #print("-------|codprod|---------", dados.codprod)

    # 38317322000131

    dados_json = json.loads(dados)
    
    teste = dados_json['CORPEM_ERP_DOC_ENT']
    #print(teste['NUMNF'])
    numnf = teste['NUMNF']

   
    
    #url = "http://serrapark.dd.spiritlinux.com:81/scripts/mh.dll/wc"
    url = "http://10.168.254.1/scripts/mh.dll/wc"

    #payload = "{\"CORPEM_ERP_MERC\": {\"CGCCLIWMS\": \"38317322000131\", \"PRODUTOS\": [{\"CODPROD\": \"11106\", \"NOMEPROD\": \"IMPRESSORA EPSON MATRICIAL FX890 BLACK - C11C524142\", \"TPOLRET\": \"0\", \"IWS_ERP\": \"0\", \"IAUTODTVE\": \"0\", \"QTDDPZOVEN\": \"0\", \"ILOTFAB\": \"0\", \"IDTFAB\": \"0\", \"IDTVEN\": \"0\", \"INSER\": \"1\", \"CODFAB\": \"L117079B\", \"NOMEFAB\": \"\", \"ITENS\": [{\"CODUNID\": \"FR\", \"FATOR\": \"1\", \"CODBARRA\": \"010343913981\", \"PESOLIQ\": \"0.000\", \"PESOBRU\": \"14.000\", \"ALT\": \"18\", \"LAR\": \"44\", \"COMP\": \"36\", \"VOL\": 1}]}]}}"
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
            notas = NotasFiscais.objects.get(nNF = numnf)
            notas.status = 2
            notas.save()
        else:
            print("#### erro ####",response.text.encode('utf-8'))
            #print()


    filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    #print("----filename1----", filename1)
    filename2 = 'Notas-'+ numnf + '-' +filename1+'.json'
    filename3 = 'NFEnviadas'+ numnf + '-' +filename1+'.txt'
    #print("----filename2----", filename2)

    #with open('uploadnf/log/notaenviada.txt', 'a', encoding="utf-8") as f:
    with open('uploadnf/log/' + filename3, 'a', encoding="utf-8") as f:
        f.write(payload)
        f.write(url)


    with open('uploadnf/log/' + filename2, 'a' , encoding="utf-8") as f:
        #f.write(json.dumps(response.text))
        f.write(response.text)
        
        print("salvou....")
        
        print("salvou....")


    
    print('passou por aqui..')
       
    return response
   
