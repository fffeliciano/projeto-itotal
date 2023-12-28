import os, sys

projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','inventario.settings')
django.setup()



from datetime import datetime
from fornecedor.models import NotasFiscais, Itens, Sku
import xmltodict

import xml.etree.ElementTree as ET
import json

from uploadnf.fornecedor.nfentrada import gerarNFentrada

import logging

logger = logging.getLogger(__name__)

logger.info("Testar programa de leitura de xml - início")

def lerxml(name_file):
    with open("xml/" + str(name_file), "rb") as f:
        doc = xmltodict.parse(f, xml_attribs=True)
      
        x = doc["nfeProc"]["NFe"]["infNFe"]["det"]

        #Verificar se é list ou dict
        if isinstance(x,list):

            for i in x:

                v_ean = i["prod"]["cEAN"]
                logger.info(f'verificando v_ean {v_ean} ')
                if v_ean.isdigit():
                    vean = int(v_ean)
                    logger.info("v_ean é digito")
                else:
                    vean = 0
                    logger.info("vean = 0 Zero")

                logger.info("passando pela verificação o CEAN do xml da NF")
                #vean = int(i["prod"]["cEAN"])

                vxProd = i["prod"]["xProd"]

                prod = {}
                prod["ean"] = f'{vean:013}'
                prod["nomeProduto"] = vxProd

                logger.info(f'valor de prod[ean] = {prod["ean"]}')
                if Sku.objects.filter(ean = prod["ean"]).exists():
                    print("---Sim já estava cadastrado -----")
                    logger.info(f'produto já estava cadastrado')
                elif prod["ean"] == '0000000000000':
                    print("--- sem ean ---")
                    logger.info(f'Valor do ean da nf {prod["ean"]}')
                    logger.info(f'Valor do ean da nf {vean}')
                else:
                    print("---Não Existe-----")
                    
                    m = Sku(**prod)
                    m.save()
                
                continue
                            
            
            

        else:
            v_ean = doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["cEAN"]

            if v_ean.isdigit():
                vean = int(v_ean)
            else:
                vean = 0

            vxProd = doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["xProd"]
      
	
            prod = {}

            prod["ean"] = f'{vean:013}'
            prod["nomeProduto"] = vxProd
        
            if Sku.objects.filter(ean = prod["ean"]).exists():
                print("---Sim Existe-----")
            elif prod["ean"] == '0000000000000':
                print("---2) somente numero zero 13 vezes")
            else:
                print("---Não Existe-----")
                
                m = Sku(**prod)
                m.save()

    return(doc)
    



resultado = lerxml("42220801763720000171550050007743841453840194.xml")

data = gerarNFentrada(resultado)

