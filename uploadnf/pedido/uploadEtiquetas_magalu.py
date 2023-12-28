import os, sys

projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','inventario.settings')
django.setup()


from pdf2image import convert_from_path
from PIL import Image

import platform

#----------------------------------------

#from PyPDF2 import PdfReader
import PyPDF2

import logging

logger = logging.getLogger(__name__)




from pedidos.models import Pedidos


#----------------------------------------
import pytesseract



#from pathlib import Path

from datetime import date 


import zpl 
import pickle





def processa_imagem(medidas, im, medidas1):

    imRt = im.crop((medidas))
    imRt1 = im.crop((medidas1))
    #ubuntu
    #fileNameImg = './etiquetas/nameImagem.png'
    fileNameImg = 'etiquetas/nameImagem.png'    # imagem da pagina com 3 etiquetas do ml
    fileNameImg1 = 'etiquetas/nameImagemNova.png'   # retangulo codigo rastreamento

    imRt.save(fileNameImg,"PNG")
    imRt1.save(fileNameImg1,"PNG")

    
    text = str(((pytesseract.image_to_string(Image.open(fileNameImg1)))))
    print("text___>>", text)
    texto = text.splitlines()
    print("texto da Etiqueta ?? ------>", texto)
    print(type(texto))

    #exit(90)
    
    
    if not texto :
        print("Vazio")
        # Deletar aqui os arquivos que não vou mais utilizar
        # nameImagem.png
        print("remove")
        os.remove(fileNameImg)
        os.remove(fileNameImg1)
    elif texto == ['']:
        print("Achei texto fazio de novo", texto)
        print("remover")
        os.remove(fileNameImg)
        os.remove(fileNameImg1)
    else:
        print("Tem Conteúdo, segue o jogo")

        

        for n in texto:

            print("conteúdo de n : ==>", n)
            print("conteúdo de n[12:] : ==>", n[12:].strip())
            print("len conteúdo de n[12:] : ==>", len(n[12:].strip()))



            if len(n[12:].strip()) == 5:
                #numped_mktpl = n #if n[0:2].find('0') > 0 else n[0:2].replace('0','O') + n[2:13]

                #y = n if n[0:2].find('0') > 0 else n[0:2].replace('0','O') + n[2:13]
                # w = Pedidos.objects.filter(numpedrca = numped_mktpl_base.replace(" ", "")).values('numnf')
                #  -  MyModel.objects.filter(pk=some_value).update(field1='some value')
                #  -  Pedidos.objects.filter(pk=some_value).update(Status=2)
                #  -  Alterar Model para incluir os campos de tamanho do arquivo, e o campo dados da etiqueta padrao zpl
                
                #print('número da Nota Fiscal',w)
                #y = w[0]
                #print("y ===> :", y)
                #print("y ===>", y['numnf'])
                novoNome = n[12:].strip()
                newName1 = "etiquetas/" + str(novoNome)
                newName3 = str(novoNome)
                print('novoNome ====>', novoNome)
                print('newName1 ====>', newName1)
                print('newName3 ====>', newName3)
        
                #continue
            
                print("newName1 ==>" , newName1 + ".txt")
                print(len(newName1))

                print('newName3--->>>', newName3)
                # os.remove(fileName1)
                
                


                #print("|||----- Achei nrp --->", nrp.objects)
                #exit(90)


                # Procurar o numero da NF em Pedidos - fim ---------------------------
                
                os.rename(fileNameImg, newName1 + ".png")
                os.remove(fileNameImg1)
                #os.rename(fileNameImg, newName + ".png")
                #break


                return(newName3)


#--------------------------------------------------------------------------------------------------------------


def gerarArquivos(nrNota):
    # Ubuntu 
    # Ubuntu alterar diretorio de baixo
    #fileName2 = f'C:\\ProgramData\\Anaconda3\\envs\\itotal\\etiquetas\\{nrNota}.png'
    #nrNota = '220321EHOJYHST'
    #fileName2 = f'/home/ubuntu/projeto-es/etiquetas/{nrNota}.png'
    # 
    # f'./etiquetas/{nrNota}.txt'

    #print("----------- nrNota ----------", nrNota )


    #fileName2 = f'C:\\Users\\Fernando\\anaconda3\\envs\\projetoImg\\etiquetas\\{nrNota}.png'
    #fileName2 = f'/home/ubuntu/projeto-es/etiquetas/{nrNota}.png'
    #print("*** fileName2 : ", fileName2)

    if platform.system()=='Windows':
        #fileName2 = f'C:\\ProgramData\\Anaconda3\\envs\\projeto-es\\etiquetas\\{nrNota}.png'
        fileName2 =  os.getcwd()+f'\etiquetas\{nrNota}.png'
    else:
        #fileName2 = f'/home/ubuntu/projeto-es/etiquetas/{nrNota}.png'
        fileName2 =  os.getcwd()+f'/etiquetas/{nrNota}.png'


    #C:\Users\Fernando\anaconda3\envs\projetoImg\

    #fileName1 = f'etiquetas\\{nrNota}.png'
    fileName1 = f'{nrNota}.png'
    print("*** fileName1 : ", fileName1)

    #exit(92)


    #l = zpl.Label(110  ,180)
    l = zpl.Label(110  ,180)
    height = 0

    #image_width = 180
    #! image_width = 69
    image_width = 67
    #image_width = 63 # ( Aparece o numero na etiqueta )
     
    l.origin(0,0)

    path = os.getcwd()
    #path = 'C:\\ProgramData\\Anaconda3\\envs\\itotal\\etiquetas\\'
    #path = 'C:\\Users\\Fernando\\anaconda3\\envs\\projetoImg'
    #path = '/home/ubuntu/projeto-es'

    image_height = l.write_graphic(
        #Image.open(os.path.join(os.path.dirname(zpl.__file__), '2530.png')),
        Image.open(os.path.join(os.path.dirname(zpl.__file__), fileName2)),
        image_width)
    l.endorigin()

    ### Tamanho
    def utf8len(s):
        return len(s.encode('utf-8'))

    #z1 = Pedidos.objects.filter(numnf=nrNota).values('numpedrca')
    #z2 = Pedidos.objects.filter(numnf=nrNota, status=1).update(tamanhoEtiqueta=str(utf8len(l.dumpZPL())),etiquetaZPLBase64=l.dumpZPL(), status=6)
    z2 = Pedidos.objects.filter(numnf=nrNota, status=1).update(tamanhoEtiqueta=str(utf8len(l.dumpZPL())), status=6)
    #print("provável z1 = ", z1)
    print("provável z2 = ", z2)


    with open( f'./etiquetas/{nrNota}.zpl', 'w') as f:
        f.write( l.dumpZPL() )

    #print("*** file_zpl tamanho:", utf8len(l.dumpZPL()))

    # Salvar o tamanho do arquivo , para enviar junto com a NotaFiscalComplementar.py 
    with open( f'./etiquetas/{nrNota}.txt', 'w') as f:
        f.write( str(utf8len(l.dumpZPL())) )

    os.remove("etiquetas/" + fileName1)


    return




#-------------------------------------------------------------------------------------------------------------



def lerEtiquetas_magalu(name_file):

    logger.info("Rodando lerEtiquetas Mercado Livre")
    logger.info("name_file--> {a} ".format(a=name_file))

    cwd = os. getcwd()
    logger.info("diretório atual ==> {b} ".format(b=cwd))
 
    #images = convert_from_path(name_file, 500)
    if platform.system()=="Windows":
        images = convert_from_path(name_file, 500,poppler_path=r'C:\Program Files\poppler-0.68.0\bin') 
    else: 
        images = convert_from_path(name_file, 500)

    tamanho = len(images)
    #print("tamanho arquivo images ::", tamanho)
    #print(enumerate(images))

    for i, image in enumerate(images):

        if platform.system()=='Windows':
            diretorio = 'etiquetas\\'
        else:
            diretorio = 'etiquetas/'

        fname = diretorio+'image'+str(i)+'.png'
        
        fnameRetangulo = diretorio+'image-retangulo'+str(i)+'.png'
        

        #fname = 'etiquetas/image'+str(i)+'.png'
        #fnameRetangulo = 'etiquetas/image-retangulo'+str(i)+'.png'
        
        #print("criando o arquivo :", fname)
        logger.info("criando o arquivo : {d}".format(d=fname))
        image.save(fname, "PNG")

        
        # Criar um if abaixo, e avaliar um retangulo se tem o texto "Declaração"
        # se tiver Declaração rodar com o "continue"


        # Opens a image in RGB mode
        #im = Image.open(f"C:\\Users\\Fernando\\anaconda3\\envs\\projetoImg\\{fname}")
        #im = Image.open(f"/home/ubuntu/projeto-es/{fname}")
        if platform.system()=='Windows':
            im = Image.open(f"C:\\Users\\FernandoFeliciano\\anaconda3\\envs\\projeto-es\\{fname}")
        else:
            im = Image.open(f"/home/ubuntu/projeto-es/{fname}")

        #print("1)valor de ", i)

        width, height = im.size
        print("width, height -->", width, height)



        ###############
        # Etiqueta 1
        ###############
        # medidas da primeira etiqueta, a4 , lado esquerdo, canto superior
        # top da etiqueta pegar o numero do pedido
        medidas = [0,0,2067,2924]
        medidas1 = [860,890,1440,960]
        #print("# Etiqueta 1")
        #print("medidas :", medidas)
        #print("medidas1 :", medidas1)

        testar = processa_imagem(medidas, im, medidas1)

        if(testar is not None):
            #print("testar is not None")
            gerador = gerarArquivos(testar)
        #print("Fim etiqueta 1...")


        
        ###############
        # Etiqueta 2
        ###############
        # medidas da segunda etiqueta, a4 , lado esquerdo, canto inferior
        medidas = [2067,0,4134,2924]
        medidas1 = [2870,890,3430,960]
        #print(" Etiqueta 2")
        #print("medidas :", medidas)
        #print("medidas1 :", medidas1)

        testar = processa_imagem(medidas, im, medidas1)

        #print("testar :", testar)
        
        if(testar is not None):
            #print("testar is not None")
            gerador = gerarArquivos(testar)

        #print("Fim etiqueta 2...")
        

        ###############
        # Etiqueta 3
        ###############
        # medidas da terceira etiqueta, a4 , lado direito, canto superior
        medidas = [0,2925,2067,5847]
        medidas1 = [860,3770,1440,3840]
        #print("# Etiqueta 3")
        #print("medidas :", medidas)
        #print("medidas :", medidas1)

        testar = processa_imagem(medidas, im, medidas1)

        #print("testar :", testar)

        if(testar is not None):
            #print("testar is not None")
            gerador = gerarArquivos(testar)
        
        #print("Fim etiqueta 3...")

        ###############
        # Etiqueta 4
        ###############
        # medidas da quarta etiqueta, a4 , lado direito, canto inferior
        medidas = [2067,2925,4134,5847]
        medidas1 = [2870,3770,3430,3840]
        #print("# Etiqueta 4")
        #print("medidas :", medidas)
        #print("medidas :", medidas1)


        testar = processa_imagem(medidas, im, medidas1)
        #print("testar :", testar)
        if(testar is not None):
            print("testar is not None")
            gerador = gerarArquivos(testar)

        #print("Fim etiqueta 4...")

    #! os.remove(fname)
    
    return()
    
#ml_etiquetas_ml_2.pdf
#z = lerEtiquetas_ml("xml/ml_etiquetas_ml_1.pdf")


# z = lerEtiquetas_magalu("xml/Magalupreto110820230849_FYwbmAl.pdf")
# Magalupreto110820230849_FYwbmAl.pdf
#ml_etiquetas_1_05-10-2022

