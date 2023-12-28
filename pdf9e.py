from pdf2image import convert_from_path
from PIL import Image



#----------------------------------------
import sys
import os
import django
#from PyPDF2 import PdfReader
import PyPDF2

import logging

logger = logging.getLogger(__name__)


os.environ.setdefault('DJANGO_SETTINGS_MODULE','inventario.settings')

django.setup() #run django.setup BEFORE importing modules to setup the environ


from pedidos.models import Pedidos


#----------------------------------------
import pytesseract



#from pathlib import Path

from datetime import date 


import zpl 
import pickle





def processa_imagem(medidas, im):

    imRt = im.crop((medidas))
    #ubuntu
    #fileNameImg = './etiquetas/nameImagem.png'
    fileNameImg = 'etiquetas/nameImagem.png'

    imRt.save(fileNameImg,"PNG")

    #exit(80)

    indices = [1,2,3,4,5,6,7,8,9,10]
    todays_date = date.today()

    ano = todays_date.year - 2000
    mes = f"{todays_date.month:02d}"
    if todays_date.month == 1:
            anoAnt = todays_date.year - 2001
            mesAnt = f"{todays_date.month + 11:02d}"  # todays_date.month + 11
            #print("tipo ano", type(anoAnt))
    else:
            anoAnt = todays_date.year - 2000
            mesAnt = f"{todays_date.month - 1:02d}"   #todays_date.month - 1
            #print("tipo ano", type(anoAnt))

    anomes = str(ano) + str(mes)
    anomesAnt = str(anoAnt) + str(mesAnt)

    
    text = str(((pytesseract.image_to_string(Image.open(fileNameImg)))))
    texto = text.splitlines()
    print("texto ------>", texto)
    if not texto :
        print("Vazio")
        # Deletar aqui os arquivos que não vou mais utilizar
        # nameImagem.png
        print("remove")
        os.remove(fileNameImg)
    elif texto == ['']:
        print("Achei texto fazio de novo", texto)
        print("remover")
        os.remove(fileNameImg)
    else:
        print("Tem Conteúdo, segue o jogo")

        select_elements1 = [texto[index] for index in indices]

        

        for n in select_elements1:
            
            if str(n[0:4]) == anomes:
                print("*********** BINGO *************")
                print(n)
                print(n[0:4])
                print(type(n[0:4]))
                #newName1 = "etiquetas/" + n
                newName3 = n
            elif str(n[0:4]) == anomesAnt :
                print("############### Bingo 2 ###########")
                print(n)
                print(n[0:4])
                print(type(n[0:4]))
                #newName1 = "etiquetas/" + n
                newName3 = n
            else: 
                #print("nada a haver")
                continue
            
            # print(newName1 + ".txt")
            # print(len(newName1))
            # os.remove(fileName1)
            
            # Procurar o numero da NF em Pedidos - início ------------------------

            #Pedidos.objects
            #print('newName3--->>>', newName3)
            #nrp = Pedidos(numpedrca = newName3 )


            #t=Pedidos.objects.all()
            #print("db Pedidos all()", t)   
            n = Pedidos.objects.filter(numpedrca = newName3).values('numnf')
            y = n[0]
            print("y ===> :", y)
            print("y ===>", y['numnf'])
            novoNome = y['numnf']
            newName1 = "etiquetas/" + str(novoNome)
            newName3 = str(novoNome)

            print("newName1 ==>" , newName1 + ".txt")
            print(len(newName1))

            print('newName3--->>>', newName3)
            # os.remove(fileName1)
            



            #print("|||----- Achei nrp --->", nrp.objects)
            #exit(90)


            # Procurar o numero da NF em Pedidos - fim ---------------------------
            
            os.rename(fileNameImg, newName1 + ".png")


            return(newName3  )


#--------------------------------------------------------------------------------------------------------------


def gerarArquivos(nrNota):
    # Ubuntu 
    # Ubuntu alterar diretorio de baixo
    #fileName2 = f'C:\\ProgramData\\Anaconda3\\envs\\itotal\\etiquetas\\{nrNota}.png'
    #nrNota = '220321EHOJYHST'
    #fileName2 = f'/home/ubuntu/projeto-es/etiquetas/{nrNota}.png'
    #
    # 
    # f'./etiquetas/{nrNota}.txt'

    print("----------- nrNota ----------", nrNota )


    #fileName2 = f'C:\\Users\\Fernando\\anaconda3\\envs\\projetoImg\\etiquetas\\{nrNota}.png'
    fileName2 = f'/home/ubuntu/projeto-es/etiquetas/{nrNota}.png'
    print("*** fileName2 : ", fileName2)


    #C:\Users\Fernando\anaconda3\envs\projetoImg\

    #fileName1 = f'etiquetas\\{nrNota}.png'
    fileName1 = f'{nrNota}.png'
    print("*** fileName1 : ", fileName1)

    #exit(92)


    l = zpl.Label(110  ,180)
    height = 0

    #image_width = 180
    image_width = 69
        
    l.origin(0,0)


    #path = 'C:\\ProgramData\\Anaconda3\\envs\\itotal\\etiquetas\\'

    #path = 'C:\\Users\\Fernando\\anaconda3\\envs\\projetoImg'
    path = '/home/ubuntu/projeto-es'

    #print("conteúdo do fileName2", fileName2)

    image_height = l.write_graphic(
        #Image.open(os.path.join(os.path.dirname(zpl.__file__), '2530.png')),
        Image.open(os.path.join(os.path.dirname(zpl.__file__), fileName2)),
        image_width)
    l.endorigin()



    ### Tamanho
    def utf8len(s):
        return len(s.encode('utf-8'))



    with open( f'./etiquetas/{nrNota}.zpl', 'w') as f:
        f.write( l.dumpZPL() )


    #print("*** file_zpl tamanho:", utf8len(l.dumpZPL()))

    # Salvar o tamanho do arquivo , para enviar junto com a NotaFiscalComplementar.py 
    with open( f'./etiquetas/{nrNota}.txt', 'w') as f:
        f.write( str(utf8len(l.dumpZPL())) )



    #exit(90)
    # PAREI AQUI NA LINHA DE BAIXO , QUE FOI COMENTADA
    # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'




    #print("Name File recebido (fileImg) ", fileImg)



    #pathFile = '.\\etiquetas\\' + fileImg
    #print("--- pathFile --->", pathFile )

    print(" fileName1 conteúdo :", fileName1)


    #teste = pytesseract.image_to_string( Image.open("./etiquetas/" + fileName1) )
    teste = pytesseract.image_to_string( Image.open("etiquetas/" + fileName1) )
    new_teste = teste.split('\n')
    print(new_teste)

    
    #exit(88)

    #with open( f'./etiquetas/{nrNota}-dadosetq.txt' , 'wb' ) as temp:
    with open( f'etiquetas/{nrNota}-dadosetq.txt' , 'wb' ) as temp:
        print("Vou salvar arquivo dados da etiqueta")
        pickle.dump(new_teste, temp)

    os.remove("etiquetas/" + fileName1)


    return




#-------------------------------------------------------------------------------------------------------------



#def lerEtiquetas_shopee(name_file):

logger.info("Rodando lerEtiquetas_shopee")
#logger.info("name_file--> {a} ".format(a=name_file))

cwd = os. getcwd()
logger.info("diretório atual ==> {b} ".format(b=cwd))
"""
with open(name_file, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    #logger.info("doc--> {a} ".format(a=uploaded_file))
    logger.info("Number of Pages in PDF File is {a} ".format(a=pdf_reader.getNumPages()))
    logger.info("PDF Metadata is {b}".format(b= pdf_reader.documentInfo))
    logger.info("conteúdo pdf_reader {c}".format(c=pdf_reader))
"""





# shopee-23-03-2022
#images = convert_from_path("shopee-23-03-2022.pdf", 500,poppler_path=r'C:\Program Files (x86)\poppler\poppler-0.68.0_x86\poppler-0.68.0\bin')
images = convert_from_path("xml/etiquetas-shopee-16578892962191.pdf", 500)
#images = convert_from_path(name_file, 500)
#images = convert_from_path(pdf"shopee-03-04-2022.pdf", 500,poppler_path=r'C:\Program Files (x86)\poppler\poppler-0.68.0_x86\poppler-0.68.0\bin')
#images = convert_from_path("shopee-04-04-2022.pdf", 500,poppler_path=r'C:\Program Files (x86)\poppler\poppler-0.68.0_x86\poppler-0.68.0\bin')




tamanho = len(images)
print(tamanho)
#print(enumerate(images))

#exit(90)


for i, image in enumerate(images):

    print("Definindo o nome do arquivo, passagem :", i)

    # Definindo o nome dos arquivos
    print("3)valor de i :", i)
    #fname = './etiquetas/image'+str(i)+'.png'
    fname = 'etiquetas/image'+str(i)+'.png'
    #fnameRetangulo = './etiquetas/image-retangulo'+str(i)+'.png'
    fnameRetangulo = 'etiquetas/image-retangulo'+str(i)+'.png'
    

    
    #image.save(fname, "PNG")
    #print("criando o arquivo :", fname)
    logger.info("criando o arquivo : {d}".format(d=fname))
    image.save(fname, "PNG")

    #exit(90)
    #print(fname, fname2, fname3)
    
    # Criar um if abaixo, e avaliar um retangulo se tem o texto "Declaração"
    # se tiver Declaração rodar com o "continue"


    # Opens a image in RGB mode
    #im = Image.open(f"C:\\Users\\Fernando\\anaconda3\\envs\\projetoImg\\{fname}")
    im = Image.open(f"/home/ubuntu/projeto-es/{fname}")

    print("1)valor de ", i)
    #if i > tamanho - 3 :
    #    print("2)valor de ", i)
    #    continue


    

    #arquivo_upload = 'shopee-26-03-2022.pdf'
    #print("Arquivo extenção = ", arquivo_upload.suffix)
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)



    width, height = im.size
    print("width, height -->", width, height)

    # Medição do Retangulo
    left = 0
    top = 0
    right = 5840
    bottom = 460

    imRetangulo = im.crop((left, top, right, bottom))

    imRetangulo.save(fnameRetangulo,"PNG")

    text = str(((pytesseract.image_to_string(Image.open(fnameRetangulo)))))
    text1 = text.splitlines()  

    print("remove retangulo")
    os.remove(fnameRetangulo)

    if "DECLARACAO DE CONTEUDO" in text1 :
        print("achei a declaração!")
        print("remove arquivo :", fname)
        os.remove(fname)
        break
    else:
        print("não achei a Declaração")

    



    ###############
    # Etiqueta 1
    ###############
    # medidas da primeira etiqueta, a4 , lado esquerdo, canto superior
    medidas = [0,0,2066,2920]
    print("medidas :", medidas)

    testar = processa_imagem(medidas, im)

    print("testar :", testar)


    if(testar is not None):
        print("testar is not None")
        gerador = gerarArquivos(testar)


    
    ###############
    # Etiqueta 2
    ###############
    # medidas da segunda etiqueta, a4 , lado esquerdo, canto inferior
    medidas = [0,2921,2066,5840]
    print("medidas :", medidas)

    testar = processa_imagem(medidas, im)

    print("testar :", testar)
    
    if(testar is not None):
        print("testar is not None")
        gerador = gerarArquivos(testar)




    ###############
    # Etiqueta 3
    ###############
    # medidas da terceira etiqueta, a4 , lado direito, canto superior
    medidas = [2067,0,4132,2920]
    print("medidas :", medidas)

    testar = processa_imagem(medidas, im)

    print("testar :", testar)

    if(testar is not None):
        print("testar is not None")
        gerador = gerarArquivos(testar)

    ###############
    # Etiqueta 4
    ###############
    # medidas da quarta etiqueta, a4 , lado direito, canto inferior
    medidas = [2067,2921, 4132,5840]
    print("medidas :", medidas)

    testar = processa_imagem(medidas, im)

    print("testar :", testar)

    if(testar is not None):
        print("testar is not None")
        gerador = gerarArquivos(testar)



    print("remover o file : ", fname)
    os.remove(fname)

#return()
    
 
#z = lerEtiquetas_shopee("xml/shopee-24-06-2022-1.pdf")