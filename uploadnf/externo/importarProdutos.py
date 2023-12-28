import os, sys

projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

from uploadnf.pedido import testarPost
import json, requests, urllib
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta


#----------------------------------------------

load_dotenv()
BLING_SECRET_KEY = os.getenv("BLING_API_KEY")

#N = 90

# n numero de dias atras.
n = 30

date_N_days_ago = datetime.now() - timedelta(days=n)
#date.today()

date_inicio_formated = date_N_days_ago.strftime("%d/%m/%Y")

date_fim_formated = datetime.now().strftime("%d/%m/%Y") 

periodo = []
periodo1 = date_inicio_formated
periodo2 = date_fim_formated
situcacao = 'A'
tipo = 'P'

print("Periodo escolhido ",periodo1, periodo2)

#exit(99)

#--------------------------------------------------------------------- excluir/comentar estas linhas
#periodo1 = "02/09/2021"
#periodo2 = "02/09/2021"
#--------------------------------------------------------------------- excluir/comentar estas linhas




n = 1
    
while True:
    url = f"https://bling.com.br/Api/v2/produtos/page={n}/json/"



    payload = {
        "apikey": BLING_SECRET_KEY,
        "filters": f"dataAlteracao[{periodo1} TO {periodo2}]; \
        situacao[{situcacao}]; \
        tipo[{tipo}]",
    }

    try:
        response = requests.get(url, params=payload)

        dados = json.loads(response.content)
        
        #print(response.status_code)

        if response.status_code == 200:
            #print("status 200")
            dados = json.loads(response.content)


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


    if response == 200:
        continue

    if "erros" in datas:
        print("===== achei erro 14 =====>")
        break


    #response = requests.get(url, params=payload)
    #dados = json.loads(response.content)

    #print(dados)

    class Produto(object):
        def __init__(self, id, codigo, descricao, tipo, situacao, unidade, preco, precoCusto, descricaoCurta, descricaoComplementar, dataInclusao, dataAlteracao, imageThumbnail, urlVideo, nomeFornecedor, codigoFabricante, marca, class_fiscal, cest, origem, idGrupoProduto, linkExterno, observacoes, grupoProduto, garantia, descricaoFornecedor, idFabricante, categoria, pesoLiq, pesoBruto, estoqueMinimo, estoqueMaximo, gtin, gtinEmbalagem, larguraProduto, alturaProduto, profundidadeProduto, unidadeMedida, itensPorCaixa, volumes, localizacao, crossdocking, condicao, freteGratis, producao, dataValidade, spedTipoItem ):
            self.codprod = codigo
            self.nomeprod = descricao[0:99]
            self.tpolret = 0
            self.iws_erp = 0 
            self.iautodtven = 0
            self.qtddpzoven = 0
            self.ilotfab = 0
            self.idtfab = 0
            self.idtven = 0
            self.inser = 1
            self.codfab = codigoFabricante
            self.nomefab = marca
            self.status = situacao



        @classmethod
        def from_json(cls, json_string):
            json_dict = json.loads(json_string)
            return cls(**json_dict)
            #return cls(**json_string)



        def __repr__(self):
            return f'<sku {self.codprod}>' 

    
    class Embalagem(object):
        def __init__(self, id, codigo, descricao, tipo, situacao, unidade, preco, precoCusto, descricaoCurta, descricaoComplementar, dataInclusao, dataAlteracao, imageThumbnail, urlVideo, nomeFornecedor, codigoFabricante, marca, class_fiscal, cest, origem, idGrupoProduto, linkExterno, observacoes, grupoProduto, garantia, descricaoFornecedor, idFabricante, categoria, pesoLiq, pesoBruto, estoqueMinimo, estoqueMaximo, gtin, gtinEmbalagem, larguraProduto, alturaProduto, profundidadeProduto, unidadeMedida, itensPorCaixa, volumes, localizacao, crossdocking, condicao, freteGratis, producao, dataValidade, spedTipoItem   ):
            self.codunid = "PC"
            self.fator = "1"
            self.codbarra = gtin
            self.pesoliq = float(pesoLiq)
            self.pesobru = float(pesoBruto)
            
            if not alturaProduto:
                alturaProduto = 0
            if type(alturaProduto) == int:
                self.alt = int(float(alturaProduto))
            elif type(alturaProduto) == str:
                self.alt = int(float(alturaProduto.replace(",",".")))

            if not larguraProduto:
                larguraProduto=0
            if type(larguraProduto) == int:
                self.lar = int(float(larguraProduto))
            elif type(larguraProduto) == str:
                self.lar = int(float(larguraProduto.replace(",",".")))

            if not profundidadeProduto:
                profundidadeProduto = 0
            if type(profundidadeProduto) == int:
                self.comp = int(float(profundidadeProduto))
            elif type(profundidadeProduto) == str:
                self.comp = int(float(profundidadeProduto.replace(",",".")))








            #if alturaProduto is not None:
                #print("altura===>",alturaProduto)
                #self.alt = int(float(alturaProduto))
		#
                #print("altura===>",alturaProduto.replace(",", "."))
                #self.alt = int(float(alturaProduto.replace(",", ".")))

            #if larguraProduto is not None:
                #print("largura===>",larguraProduto.replace(",", "."))
                #self.lar = int(float(larguraProduto.replace(",", ".")))

            #if not profundidadeProduto:
                #profundidadeProduto = 0
            #if profundidadeProduto is not None:
                #print("Profundidade===>",profundidadeProduto.replace(",", "."))
                #self.comp = int(float(profundidadeProduto.replace(",", ".")))

            if not volumes:
                volumes = 1
            if volumes is not None:
                print("volumes===>",volumes)
                self.vol = int(float(volumes))
        

        @classmethod
        def from_json(cls, json_string):
            json_dict = json.loads(json_string)
            return cls(**json_dict)


        def __repr__(self):
            return f'<ean {self.codbarra}>' 



    dados_list = []
    
    #print(dados)
    

    for u in dados['retorno']['produtos']:
        i = json.dumps(u['produto'])

        if "estrutura" in i:
            continue

        if "variacoes" in i:
            continue

        if "clonarDadosPai" in i:
            continue

        #print("-------------------------- v1 ----------------")

        prod = Produto.from_json(i)

        #print(Embalagem.from_json(i))
        emb = Embalagem.from_json(i)

        jsonStr = json.dumps(prod.__dict__)

        jsonStrEmb = json.dumps(emb.__dict__)


        jsonDict = json.loads(jsonStr)

        JsonDictEmb = json.loads(jsonStrEmb)

        myDict3 = {}
        myDict3["embalagens"] = [JsonDictEmb]

        jsonDict.update(myDict3)

        #print("-------------------------- v2 ----------------")

        print(json.dumps(jsonDict))

        #resultado_retorno = testarPost.AddBase(json.dumps(jsonDict))
        resultado_retorno = testarPost.AddBase(jsonDict)

        print(resultado_retorno)

    n = n+1
