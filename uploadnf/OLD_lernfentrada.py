from datetime import datetime
from fornecedor.models import NotasFiscais, Itens, Sku
import xmltodict

import xml.etree.ElementTree as ET
import json




def lerxml(name_file):
    with open("xml/" + str(name_file), "rb") as f:
        doc = xmltodict.parse(f, xml_attribs=True)
      
        x = doc["nfeProc"]["NFe"]["infNFe"]["det"]

        #Verificar se é list ou dict
        if isinstance(x,list):

            for i in x:

                vean = i["prod"]["cEAN"]
                vxProd = i["prod"]["xProd"]

                prod = {}
                prod["ean"] = vean
                prod["nomeProduto"] = vxProd

                print(i["prod"]["cEAN"])
                print(i["prod"]["xProd"])

                            
                if Sku.objects.filter(ean = prod["ean"]).exists():
                    print("---Sim já estava cadastrado -----")
                else:
                    print("---Não Existe-----")
                    
                    m = Sku(**prod)
                    m.save()
                
                continue
                            
            
            

        else:
            vean = doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["cEAN"]
            vxProd = doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["xProd"]

            print(doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["cEAN"])
            print(doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]["xProd"])

            prod = {}

            prod["ean"] = vean
            prod["nomeProduto"] = vxProd
        
            if Sku.objects.filter(ean = prod["ean"]).exists():
                print("---Sim Existe-----")
            else:
                print("---Não Existe-----")
                
                m = Sku(**prod)
                m.save()

    return(doc)
    

