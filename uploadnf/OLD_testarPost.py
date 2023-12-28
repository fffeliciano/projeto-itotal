import requests
import json
import time
import datetime



#testarPost.AddNota
def AddNota(dados):
    
    #print("rodando AddNota")
    #print()

    #print(" -----AddBasePedidos--dados---->>>>>", dados)
    time.sleep(2)
    url = "http://localhost:8000/fornecedor/"
            
    headers = {
    'authorization': "Token 4e9c2dcad540a9139c79ee6e6a91b0b09d0b467f",
    'content-type': "application/json; charset=UTF-8;",
    'cache-control': "no-cache",
    'postman-token': "f63f85ca-212a-b6c3-0497-7322f53ada91"
    }
  

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

    with open(filename, 'a', encoding="utf-8") as fd:
        
        fd.write(v)
        fd.write("\n")
        if z > 220:
            fd.write(json.dumps(dados))
            fd.write("\n")
        

    return(response)