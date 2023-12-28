import os, sys

#exit(94)

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

import pdfkit

import logging
logger = logging.getLogger(__name__)
logger.info("teste de passagem importarNotaFiscalComplemento - 2")




#path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
path_wkhtmltopdf = r"/usr/local/bin/wkhtmltopdf"

config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
#config = pdfkit.configuration(mkhtmltopdf='/usr/local/bin/wkhtmltopdf')
#usr/bin/wkhtmltopdf



#----------------------------------------------

load_dotenv()
BLING_SECRET_KEY = os.getenv("BLING_API_KEY")
#N = 90

# n numero de dias atras.
n = 1


x = datetime.now()

#if int(x.strftime("%H")) > 2:
#    n = 0
#else:
#    n = 1

if x.weekday() == 0:
    n = 5
elif int(x.strftime("%H")) > 14:
    n = 2
else:
    n = 2




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
#periodo1 = "01/10/2022"
#periodo2 = "26/10/2022"
#--------------------------------------------------------------------- excluir/comentar estas linhas

print("-- Periodo 1", periodo1)
print("-- Periodo 2", periodo2)




db = "/pedidos/notasfiscais/"

retorno_djg = con_ittPedidos(date_inicio_itt, db)




print("retorno_djg===>", retorno_djg)





pdd_ittset = set(retorno_djg)
#print("pdd_itt--->", pdd_ittset)

situacao_id= "9"
tipo = "S"

n = 1

lista_pdd_bling = []

while True:

    url = f"https://bling.com.br/Api/v2/notasfiscais/page={n}/json/"

    '''
    payload = {
        "apikey": BLING_SECRET_KEY,
        "filters": f"dataEmissao[{periodo1} TO {periodo2}]; \
        idSituacao[{situacao_id}]"; \
        tipo[{situacao_id}]",
    }
    '''

    payload = {
        "apikey": BLING_SECRET_KEY,
        "filters": f"dataEmissao[{periodo1} TO {periodo2}]",
    }


    print("payload---->",   payload)

    



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

    print("data----->", data)

    


    if response == 200:
        continue

    if "erros" in datas:
        print("===== achei erro 14 =====>")
        break


    

    # checar aqui se a lista de numero de pedido tem algum registo no Model do Django pdd_ittset (Linha 45)
   
    dd_numPed_acumulado = []
    for o in dados['retorno']['notasfiscais']:
        dd = o['notafiscal']
        print("--- dd ----->", dd)
        dd_numPed_acumulado.append(dd['numero'])
        print("--- dd ----->", dd['numero'])
        print("---- dd_numPed_acumulado", dd_numPed_acumulado)


    #exit(90)
        
    pedd_bling_num = set(dd_numPed_acumulado)

    #print("pedd_bling_num --->", pedd_bling_num)
       
    conj = (pedd_bling_num - pdd_ittset)  # Um conjunto de pedidos do bling (-) conjunto de pdd db itotal)
   
    print("--- bling --pedd_bling_num -------->", pedd_bling_num)
    print("--- mysql - localhost -- pdd_ittset --->>>", pdd_ittset)


    print("--- conj ----------->>", conj)


    #exit(54)



    #dd_pedido_acumulado = []
    for u in dados['retorno']['notasfiscais']:
        dd_notafiscal ={}
       

        i = json.dumps(u['notafiscal'])
        j = u['notafiscal']
        notafiscal = u['notafiscal']
        print("print Notafiscal ==>", notafiscal)
        


        if notafiscal['cfops'] == ['6202']:
            continue
        
        t = notafiscal['transporte']

        if 'transportadora' in t:
            print("||| SIM EXISTE TRASNPORTADORA")
        else:
            print("||| NAO EXISTE TRANSPORTADORA")
            continue
        
        
        print("*** t ***", t)
        print("*** cgc ***", t['cnpj'])

        t.setdefault('cnpj','0')
        print("&&& t &&& :",t)
        #exit(90)



        logger.info(f'valor da variável t : {t}')


        #t1 = t.setdefault('cnpj','00')
        t1 = t['cnpj']

        print("--- t1 --cgc transportadora-->>>  :", t1)

        print("---- u ---->", u)


        #exit(95)
        stc = u['notafiscal']['situacao']
        if stc == 'Pendente':
            continue
            print("*** Não era para imprimir nenhum texto aqui. analisando situação do pedido")

        print("==== situação do pedido ===>>", stc)


        logger.info( f'********  ----- tranporte ------ **********>>>>> {t1}')

        #print("----- cnpj transportadora ----", cnpj_transporte)


        #exit(90)


        

        codNfSerie = notafiscal['numero']+"-"+notafiscal['serie']

        print("notafiscal ----->", notafiscal)
        print("****  Print i ******" , notafiscal['numero'])

        print("--------- numero e série -1---------", codNfSerie)


        #exit(44)
        print("link danfe *>", notafiscal['linkDanfe'])
        print("chave nf *>", notafiscal['chaveAcesso'] )

        pdfkit.from_url( notafiscal['linkDanfe'], ('pdf/'+notafiscal['chaveAcesso']+'.pdf'), configuration=config)

        # Verificar tamanho do arquivo pdf
        fileSize = os.path.getsize(('pdf/'+notafiscal['chaveAcesso']+'.pdf'))

       
        resultado_ret = testarPost.consultarBaseNFsaida(codNfSerie, db)






        if  "Não encontrado" in resultado_ret :
            continue



        print("---------- resultado_ret ------------->>", resultado_ret)

        jsonDictRet = json.loads(resultado_ret)
        print("---------- resultado_ret dict ------------->>", jsonDictRet)



        jsonDictRet['situacao'] = notafiscal['situacao']
        jsonDictRet['danfefilename'] = notafiscal['chaveAcesso']+'.pdf'
        jsonDictRet['danfefilesize'] = str(fileSize)
        jsonDictRet['xmlNf'] = notafiscal['xml']
        jsonDictRet['linkDanfe'] =  notafiscal['linkDanfe']
        # jsonDictRet['cgc_transp'] = t1

        #jsonDictRet['status'] = 1
                #notafiscal['chaveAcesso']
            

        #print("---------- resultado_ret dict -2------------>>", jsonDictRet)
        #print("---------- resultado_ret json2------------>>", json.dumps(jsonDictRet))
        logger.info(f'resultado_ret json ----{json.dumps(jsonDictRet)}')


        resultado_retorno = testarPost.UpdateBasePedidos(codNfSerie, jsonDictRet, db)


        logger.info(f' ## resultado_retorno {resultado_retorno}')
        #print("#######  resultado_retorno ########", resultado_retorno)

    n = n+1



