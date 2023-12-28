import json, requests, urllib
import os
from dotenv import load_dotenv
from datetime import date
import datetime
import re
import logging
import base64
from base64 import b64encode



#from pedidos.models import Pedidos, Itens

def pedidoPost(dados):


    #--- Etiqueta -----------------------------------------------------
    try:
        with open( "etiquetas/" + str(dados['numnf']) +".zpl"  , "rb" ) as zpl_file:
            base64_bytes = base64.b64encode(zpl_file.read())

            newEtq = base64_bytes.decode('utf8')
            #print(newEtq)
            #exit(90)

        try:
            with open ( "etiquetas/" + str(dados['numnf']) +".txt", "r" ) as nr:
                nr_tamanho = nr.read()

                print("--- nr_tamanho --->", nr_tamanho)
        except FileNotFoundError:
           print("Arquivo não encontrado")

    except FileNotFoundError:


            print("*** Sorry, the file does not exist.")


    print("Situação do programa, passou pelo try, sem problemas")


dados = {}
dados['nome'] = 'Fernando Feliciano'
dados['numnf'] = '2472'
res = pedidoPost(dados)
