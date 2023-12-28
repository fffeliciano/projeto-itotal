import os, sys, re

projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','inventario.settings')
django.setup()


from pdf2image import convert_from_path
from PIL import Image 

import platform

import PyPDF2

#from pathlib import Path


import logging

logger = logging.getLogger(__name__)


from pedidos.models import Pedidos

import pytesseract

from datetime import date 

import zpl 
import pickle

#! Incluir linha abaixo ( no Ubunto não deve precisar, pois temos um path do pytesseract)
#! pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def processa_imagem(medidas, im):

    imRt = im.crop((medidas))
    #ubuntu
    #fileNameImg = './etiquetas/nameImagem.png'
    fileNameImg = 'etiquetas/nameImagem.png'

    imRt.save(fileNameImg,"PNG")

    #exit(80)
    
    text = str(((pytesseract.image_to_string(Image.open(fileNameImg)))))
    texto = text.splitlines()
    print("texto ------>", texto)


    new_teste = text.split('\n')
    print("texto ------>", texto)

    for i in new_teste :
        print("valor de i -->",i)



    ### inicio


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


        localizar_nt = re.compile(".*Nota fiscal:")
        print("--- localizar_nt --->", localizar_nt)

        
        filtered_list3 = list(filter(localizar_nt.match, new_teste ))
        print("--- filtered_list3 --->", filtered_list3)
        r_filtered_list3 = ''.join(filtered_list3)
        print("--- r_filtered_list3 --->", r_filtered_list3)
        localiza3 = new_teste.index(r_filtered_list3)
        print("--- localiza3 --->", localiza3 )
        nfstr = new_teste[localiza3]
        print("--- nfstr   >", nfstr)
        

        nomeArquivo = str(int(nfstr[12:18]))
        print(" nomeArquivo ===>", nomeArquivo)

        img_nameFile = str(int(nfstr[12:18]))+'.png'
        

        print("--- str(int(nfstr[12:18])) --->", str(int(nfstr[12:18])))
        print("--- img_nameFile --->", img_nameFile)
        
        #print("--- str(int(nfstr[12:18])) --->", str(int(nfstr[:-6])))
        #print("--- img_nameFile --->", img_nameFile)

        text_nameFile = str(int(nfstr[12:18]))+ "-dadosetq" + '.txt'
        print("--- text_nameFile --->", text_nameFile)





        ### fim

        """    
        if not texto :
            print("Vazio")
            # Deletar aqui os arquivos que não vou mais utilizar
            # nameImagem.png
            print("remove")
            os.remove(fileNameImg)
        else:
            print("Tem Conteúdo, segue o jogo")

            #select_elements1 = [texto[index] for index in indices]

        
        
        for n in select_elements1:
            print("entrei no for select_elements1")
            
            if str(n[0:4]) == anomes:
                print("*********** BINGO *************")
                print(n)
                print(n[0:4])
                print(type(n[0:4]))
                newName1 = "etiquetas/" + n
                newName3 = n
            elif str(n[0:4]) == anomesAnt :
                print("############### Bingo 2 ###########")
                print(n)
                print(n[0:4])
                print(type(n[0:4]))
                newName1 = "etiquetas/" + n
                newName3 = n
            else: 
                #print("nada a haver")
                continue
            
        
        newName1 = "etiquetas/" + nomeArquivo
        newName3 = nomeArquivo

        print(newName1 + ".txt")
        print(len(newName1))
        # os.remove(fileName1)
        
        os.rename(fileNameImg, newName1 + ".png")


        return(newName3)



            
        print(newName1 + ".txt")
        print(len(newName1))
        # os.remove(fileName1)
        
        os.rename(fileNameImg, newName1 + ".png")


        return(newName3  )"""     

        newName1 = "etiquetas/" + nomeArquivo
        newName3 = nomeArquivo

        print(newName1 + ".txt")
        print(len(newName1))
        # os.remove(fileName1)
        
        os.rename(fileNameImg, newName1 + ".png")


        return(newName3)

#--------------------------------------------------------------------------------------------------------------


def gerarArquivos(nrNota):
    # Ubuntu 
    # Ubuntu alterar diretorio de baixo
    #fileName2 = f'C:\\ProgramData\\Anaconda3\\envs\\itotal\\etiquetas\\{nrNota}.png'
    #nrNota = '220321EHOJYHST'
    #fileName2 = f'/home/ubuntu/projeto-es/etiquetas/{nrNota}.png'
    if platform.system()=='Windows':
        #fileName2 = f'C:\\ProgramData\\Anaconda3\\envs\\projeto-es\\etiquetas\\{nrNota}.png'
        fileName2 =  os.getcwd()+f'\etiquetas\{nrNota}.png'
    else:
        #fileName2 = f'/home/ubuntu/projeto-es/etiquetas/{nrNota}.png'
        fileName2 =  os.getcwd()+f'/etiquetas/{nrNota}.png'
    #
    # 
    # f'./etiquetas/{nrNota}.txt'

    print("----------- nrNota ----------", nrNota )


    #fileName2 = f'C:\ProgramData\Anaconda3\envs\projeto-es\etiquetas\{nrNota}.png'
    print("*** fileName2 : ", fileName2)


    #C:\Users\Fernando\anaconda3\envs\projeto-es\

    #fileName1 = f'etiquetas\\{nrNota}.png'
    fileName1 = f'{nrNota}.png'
    print("*** fileName1 : ", fileName1)

    #exit(92)
    


    l = zpl.Label(110  ,180)
    height = 0

    #image_width = 180
    image_width = 70
        
    l.origin(0,0)
    print("--- depois de image_height")

    #path = 'C:\\ProgramData\\Anaconda3\\envs\\itotal\\etiquetas\\'

    #path = 'C:\ProgramData\Anaconda3\envs\projeto-es\etiquetas'
    #path = '/home/ubuntu/projeto-es'
    path = os.getcwd()

    print("conteúdo do fileName2", fileName2)

    image_height = l.write_graphic(
        #Image.open(os.path.join(os.path.dirname(zpl.__file__), '2530.png')),
        Image.open(os.path.join(os.path.dirname(zpl.__file__), fileName2)),
        image_width)
    l.endorigin()

    print("--- antes de image_height")

    ### Tamanho
    def utf8len(s):
        return len(s.encode('utf-8'))


    #z1 = Pedidos.objects.filter(numnf=nrNota).values('numpedrca')
    z2 = Pedidos.objects.filter(numnf=nrNota, status=1).update(tamanhoEtiqueta=str(utf8len(l.dumpZPL())),etiquetaZPLBase64=l.dumpZPL(), status=6)




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


    teste = pytesseract.image_to_string( Image.open("./etiquetas/" + fileName1) )
    new_teste = teste.split('\n')
    print(new_teste)

    #exit(88)

    with open( f'./etiquetas/{nrNota}-dadosetq.txt' , 'wb' ) as temp:
        print("Vou salvar arquivo dados da etiqueta")
        pickle.dump(new_teste, temp)

    os.remove("etiquetas/" + fileName1)

    return




#-------------------------------------------------------------------------------------------------------------


def lerEtiquetas_magalu_correios(name_file):

    logger.info("name_file--> {a} ".format(a=name_file))

    cwd = os. getcwd()
    logger.info("diretório atual ==> {b} ".format(b=cwd))

    """
    with open('xml/' + name_file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    """
    if platform.system()=="Windows":
        images = convert_from_path(name_file, 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin') 
    else: 
        images = convert_from_path(name_file, 500)

    #images = convert_from_path(name_file, 500)
    #C:\Program Files\poppler-0.67.0_x86\poppler-0.67.0\bin

    #images = convert_from_path("xml/shopee-26-05-2022-1.pdf", 500 )
    #images = convert_from_path("xml/magalu-5.pdf", 500 )
    #images = convert_from_path("shopee-03-04-2022.pdf", 500,poppler_path=r'C:\Program Files (x86)\poppler\poppler-0.68.0_x86\poppler-0.68.0\bin')
    #images = convert_from_path("shopee-04-04-2022.pdf", 500,poppler_path=r'C:\Program Files (x86)\poppler\poppler-0.68.0_x86\poppler-0.68.0\bin')


    print("rodando depois de images")

    tamanho = len(images)
    print(tamanho)
    #print(enumerate(images))

    #exit(90)


    for i, image in enumerate(images):

        if platform.system()=='Windows':
            diretorio = 'etiquetas\\'
        else:
            diretorio = 'etiquetas/'

        fname = diretorio+'image'+str(i)+'.png'
        fnameRetangulo = diretorio+'image-retangulo'+str(i)+'.png'

        # Definindo o nome dos arquivos
        print("3)valor de i :", i)
        #fname = 'etiquetas\\image'+str(i)+'.png'
        fname1 = 'etiquetas\\image'+str(i)+'.png'
        #fnameRetangulo = 'etiquetas\\image-retangulo'+str(i)+'.png'
        

        
        #image.save(fname, "PNG")
        print("criando o arquivo :", fname)
        image.save(fname, "PNG")

        #exit(90)
        #print(fname, fname2, fname3)
        
        # Criar um if abaixo, e avaliar um retangulo se tem o texto "Declaração"
        # se tiver Declaração rodar com o "continue"


        # Opens a image in RGB mode
        #im = Image.open(f"C:\\ProgramData\\anaconda3\\envs\\projeto-es\\{fname}")
        #im = Image.open(f"/home/ubuntu/projeto-es/{fname1}")

        if platform.system()=='Windows':
            im = Image.open(f"C:\\Users\\FernandoFeliciano\\anaconda3\\envs\\projeto-es\\{fname}")
        else:
            im = Image.open(f"/home/ubuntu/projeto-es/{fname}")



        #print("1)valor de ", i)
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
        left = 1470
        top = 570
        right = 2550
        bottom = 680

        imRetangulo = im.crop((left, top, right, bottom))

        imRetangulo.save(fnameRetangulo,"PNG")

        text = str(((pytesseract.image_to_string(Image.open(fnameRetangulo)))))
        text1 = text.splitlines()  

        print("remove retangulo")
        print("--- Text1 --->>>", text1)


        os.remove(fnameRetangulo)
        #exit(90)
        if "LISTA DE POSTAGEM" in text1 :
            print("achei a Lista de postagem!")
            print("remove arquivo :", fname)
            os.remove(fname)
            continue
            #break
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

        #exit(90)
        

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


#z = lerEtiquetas_magalu_correios("xml/etiquetasmagalucorreiros090120232a.pdf")
