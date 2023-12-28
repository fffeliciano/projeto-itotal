import json, requests, urllib
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta


def con_ittCodProd(codprod):
    load_dotenv()
    url = "http://localhost:8000/produtos/"
    
    
    ITT_SECRET_KEY = os.getenv("ITT_API_KEY")

    #data_ago = datetime.now()-timedelta(minutes=60)
    #print(data_ago.strftime('%d/%m/%Y %H:%M'))
    #new_data = data_ago.strftime("%Y-%m-%d %H:%M")
    
    querystring = {"codprod": codprod}

    print(querystring)

    #querystring = {"updated_at__gt":"2021-02-12 13:10:00"}
    #uerystring = {"updated_at__gt":"2021-02-12 13:10:00"}


    headers = {
        'authorization': "Token 4e9c2dcad540a9139c79ee6e6a91b0b09d0b467f",
        'cache-control': "no-cache",
        'postman-token': "92d5a133-c9c6-23b2-fd36-4477447770a1"
        }

    #response = requests.request("GET", url, headers=headers, params=querystring)

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

    return response.text