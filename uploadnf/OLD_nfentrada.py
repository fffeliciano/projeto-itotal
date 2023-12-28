import json
from uploadnf.fornecedor.testarPost import AddNota


def gerarNFentrada(data):
                

        
        class NotasFiscais(object):
            def __init__(self, natOp, serie, nNF, dhEmi, chavenf, ecnpj, enome, dcnpj, dnome, vBC, vICMS, vProd, vFrete, vSeg, vDesc, vII, vIPI, vIPIDevol, vPIS, vCOFINS, vOutro, vNF ):
                
                self.chNFe = chavenf
                self.natOp = natOp
                self.serie = serie        
                self.nNF = nNF          
                self.dhEmi = dhEmi
                self.CNPJ_emit = ecnpj
                self.xNome_emit = enome
                self.vBC = vBC
                self.vICMS = vICMS
                self.vProd = vProd
                self.vFrete = vFrete
                self.vSeg = vSeg
                self.vDesc = vDesc
                self.vII = vII
                self.vIPI = vIPI
                self.vIPIDevol = vIPIDevol
                self.vPIS = vPIS
                self.vCOFINS = vCOFINS
                self.vOutro = vOutro
                self.vNF = vNF
                self.CNPJ_dest = dcnpj
                self.xNome_dest = dnome
                self.status = "emitido"

            @classmethod
            def from_json(cls, json_string):
                json_dict = json.loads(json_string)
                return cls(**json_dict)

            def __repr__(self):
                return f'<sku {self.nNF}>' 

        
        class Item(object):
            def __init__(self, cProd, cEAN, xProd, NCM, CEST, CFOP, uCom, qCom, vUnCom, vProd, cEANTrib, uTrib, qTrib, vUnTrib, indTot, numItem ):                #self.idnf = ""
                self.nItem = numItem
                self.cProd = cProd          
                self.cEAN = cEAN
                self.xProd = xProd
                self.NCM = NCM
                self.CFOP = CFOP
                self.uCom = uCom
                self.qCom = float(qCom)            
                self.vUnCom = float(vUnCom)
                self.vProd = float(vProd)          
                self.cEANTrib = cEANTrib
                self.uTrib = uTrib
                self.qTrib = float(qTrib)
                self.vUnTrib = float(vUnTrib)
                self.indTot = indTot
                self.ean = cEAN

            @classmethod
            def from_json(cls, json_string):
                json_dict = json.loads(json_string)
                return cls(**json_dict)


            def __repr__(self):
                return f'cProd {self.cProd}>'

        dadosNf = data["nfeProc"]["NFe"]["infNFe"]["ide"]
       
        valoresNf = data["nfeProc"]["NFe"]["infNFe"]["total"]["ICMSTot"]

        newDadosNf = {}
        newDadosNf['chavenf'] = data["nfeProc"]["protNFe"]["infProt"]["chNFe"]
        newDadosNf['ecnpj'] = data["nfeProc"]["NFe"]["infNFe"]["emit"]["CNPJ"]
        newDadosNf['enome'] = data["nfeProc"]["NFe"]["infNFe"]["emit"]["xNome"]
        newDadosNf['dcnpj'] = data["nfeProc"]["NFe"]["infNFe"]["dest"]["CNPJ"]	#self.CNPJ_dest = #1 CNPJ do Remetente
        newDadosNf['dnome'] = data["nfeProc"]["NFe"]["infNFe"]["dest"]["xNome"]	#self.xNome_dest = Destinatário

        newDadosNf['natOp'] = dadosNf.get('natOp')
        newDadosNf['serie'] = dadosNf.get('serie')
        newDadosNf['nNF'] = dadosNf.get('nNF')
        newDadosNf['dhEmi'] = dadosNf.get('dhEmi')

        newDadosNf['vBC'] = valoresNf.get('vBC')
        newDadosNf['vICMS'] = valoresNf.get('vICMS')
        newDadosNf['vProd'] = valoresNf.get('vProd')
        newDadosNf['vFrete'] = valoresNf.get('vFrete')
        newDadosNf['vSeg'] = valoresNf.get('vSeg')
        newDadosNf['vDesc'] = valoresNf.get('vDesc')
        newDadosNf['vII'] = valoresNf.get('vII')
        newDadosNf['vIPI'] = valoresNf.get('vIPI')
        newDadosNf['vIPIDevol'] = valoresNf.get('vIPIDevol')
        newDadosNf['vPIS'] = valoresNf.get('vPIS')
        newDadosNf['vCOFINS'] = valoresNf.get('vCOFINS')
        newDadosNf['vOutro'] = valoresNf.get('vOutro')
        newDadosNf['vNF'] = valoresNf.get('vNF')

        i = json.dumps(newDadosNf)

        x = data["nfeProc"]["NFe"]["infNFe"]["det"]
        

        if isinstance(x,list):

            acumItens = []

            for n in data["nfeProc"]["NFe"]["infNFe"]["det"]:
                numItens = {}

                numItem = n["@nItem"]
                itemDic = n["prod"]
                numItens["numItem"] = numItem
                itemDic.update(numItens)

                newItemDict = {}
                newItemDict["cProd"] = itemDic.get('cProd')
                newItemDict["cEAN"] = itemDic.get('cEAN')
                newItemDict["xProd"] = itemDic.get('xProd').replace('  ',' ')
                newItemDict["NCM"] = itemDic.get('NCM')
                newItemDict["CEST"] = itemDic.get('CEST')
                newItemDict["CFOP"] = itemDic.get('CFOP')
                newItemDict["uCom"] = itemDic.get('uCom')
                newItemDict["qCom"] = itemDic.get('qCom')
                newItemDict["vUnCom"] = itemDic.get('vUnCom')
                newItemDict["vProd"] = itemDic.get('vProd')
                newItemDict["cEANTrib"] = itemDic.get('cEANTrib')
                newItemDict["uTrib"] = itemDic.get('uTrib')
                newItemDict["qTrib"] = itemDic.get('qTrib')
                newItemDict["vUnTrib"] = itemDic.get('vUnTrib')
                newItemDict["indTot"] = itemDic.get('indTot')
                newItemDict["numItem"] = itemDic.get('numItem')

                q = json.dumps(newItemDict)

                its = Item.from_json(q)

                jsonStrIts = json.dumps(its.__dict__)

                JsonDictIts = json.loads(jsonStrIts) 
             
                acumItens.append(JsonDictIts)   


            pedd = NotasFiscais.from_json(i)

            jsonStr = json.dumps(pedd.__dict__)

            jsonDict = json.loads(jsonStr)

            myDict4= {}
            myDict4["itens"] = acumItens

            jsonDict.update(myDict4)

            resultado_retorno = AddNota(jsonDict)

        else:

            numItens = {}
            numItem = x['@nItem']
            numItens["numItem"] = numItem
            
            dadosItem = data["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]
            
            dadosItem.update(numItens)
       
            newItemDict = {}
            newItemDict["cProd"] = dadosItem.get('cProd')
            newItemDict["cEAN"] = dadosItem.get('cEAN')
            newItemDict["xProd"] = dadosItem.get('xProd')
            newItemDict["NCM"] = dadosItem.get('NCM')
            newItemDict["CEST"] = dadosItem.get('CEST')
            newItemDict["CFOP"] = dadosItem.get('CFOP')
            newItemDict["uCom"] = dadosItem.get('uCom')
            newItemDict["qCom"] = dadosItem.get('qCom')
            newItemDict["vUnCom"] = dadosItem.get('vUnCom')
            newItemDict["vProd"] = dadosItem.get('vProd')
            newItemDict["cEANTrib"] = dadosItem.get('cEANTrib')
            newItemDict["uTrib"] = dadosItem.get('uTrib')
            newItemDict["qTrib"] = dadosItem.get('qTrib')
            newItemDict["vUnTrib"] = dadosItem.get('vUnTrib')
            newItemDict["indTot"] = dadosItem.get('indTot')
            newItemDict["numItem"] = dadosItem.get('numItem')

            q = json.dumps(newItemDict)

            its = Item.from_json(q)

            jsonStrIts = json.dumps(its.__dict__)

            JsonDictIts = json.loads(jsonStrIts) 
            
            pedd = NotasFiscais.from_json(i)

            jsonStr = json.dumps(pedd.__dict__)

            jsonDict = json.loads(jsonStr)

            myDict4= {}
            myDict4["itens"] = [JsonDictIts]

            #print("---- myDict4 -------", myDict4)

            jsonDict.update(myDict4)

            print("---- jsonDict -------", json.dumps(jsonDict))

            resultado_retorno = AddNota(jsonDict)

