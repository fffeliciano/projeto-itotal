import requests
import json
import time
import datetime
 
import os
from dotenv import load_dotenv

load_dotenv()
DJG_SECRET_KEY = os.getenv("ITT_API_KEY")
#uri = "http://localhost:8000"
#uri = "https://mbp.f3system.com.br"
uri = "http://mbp.f3system.com.br"


#testarPost.AddNota
def AddNota(dados):
    
    #print("rodando AddNota")
    #print()

    #print(" -----AddBasePedidos--dados---->>>>>", dados)
    time.sleep(2)
    url = uri + "/fornecedor/nfe/" # url = "http://localhost:8000/fornecedor/nfe/"
            
    headers = {
    'authorization': DJG_SECRET_KEY,
    'content-type': "application/json; charset=UTF-8;",
    'cache-control': "no-cache",
    'postman-token': "f63f85ca-212a-b6c3-0497-7322f53ada91"
    }
  
    print("------ Print dados --antes jogar no request.POST----->>", dados)

    #response = requests.request("POST", url, data=json.dumps(dados), headers=headers)
    response = requests.request("POST", url, data=json.dumps(dados), headers=headers)

    #print(response.status_code)

    #print("nnnnnnnn json.dumps(dados) nnnnnnnnnn" ,json.dumps(dados))

    #print("====Response ===>>", response.status_code)

    x=dados['nNF']

    dtlog = datetime.datetime.now().strftime("%Y_%m_%d")
    filename = "LogFornecNF"+dtlog+".json"
    

    z=response.status_code
    today = datetime.datetime.now()
    
    v= str(today) + " - " + str(z) + " - " +  x  +  " - " + response.text

    with open("uploadnf/log/" + filename, 'a', encoding="utf-8") as fd:
        
        fd.write(v)
        fd.write("\n")
        if z > 220:
            fd.write(json.dumps(dados))
            fd.write("\n")
        

    return(response)
