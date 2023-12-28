import os, sys

projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','inventario.settings')
django.setup()


from pdf2image import convert_from_path
from PIL import Image



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


    #text_extra = str(((pytesseract.image_to_string(Image.open(fileNameImg)))))
    #print("text_extra", text_extra)
    
    text = str(((pytesseract.image_to_string(Image.open(fileNameImg1)))))
    print("text___>>", text)
    texto = text.splitlines()
    print("texto da Etiqueta ?? ------>", texto)
    print(type(texto))


    
    
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

        #select_elements1 = [texto[index] for index in indices]
        #select_elements1 = [texto[index] for index in indices]

        #print(select_elements1)
        #exit(90)
        

        for n in texto:
            print("conteudo do campo e tamanho do campo ", n, len(n))

           
            
            if len(n) == 13:
                codRastreio = n if n[0:2].find('0') > 0 else n[0:2].replace('0','O') + n[2:13]
                y = n if n[0:2].find('0') > 0 else n[0:2].replace('0','O') + n[2:13]


                w = Pedidos.objects.filter(codigo_rastreamento = codRastreio).values('numnf')
                print('número da Nota Fiscal',w)
                y = w[0]
                print("y ===> :", y)
                print("y ===>", y['numnf'])
                novoNome = y['numnf']
                newName1 = "etiquetas/" + str(novoNome)
                newName3 = str(novoNome)
                print('novoNome ====>', novoNome)
                print('newName1 ====>', newName1)
                print('newName3 ====>', newName3)
        
            
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


    #l = zpl.Label(110  ,180)
    l = zpl.Label(110  ,180)
    height = 0

    #image_width = 180
    #! image_width = 69
    image_width = 61
    #image_width = 63 # ( Aparece o numero na etiqueta )
     
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



def lerEtiquetas_ml(name_file):

    logger.info("Rodando lerEtiquetas Mercado Livre")
    logger.info("name_file--> {a} ".format(a=name_file))

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
    #images = convert_from_path("shopee-24-06-2022-1.pdf", 500)
    images = convert_from_path(name_file, 500)
    #images = convert_from_path(pdf"shopee-03-04-2022.pdf", 500,poppler_path=r'C:\Program Files (x86)\poppler\poppler-0.68.0_x86\poppler-0.68.0\bin')
    #images = convert_from_path("shopee-04-04-2022.pdf", 500,poppler_path=r'C:\Program Files (x86)\poppler\poppler-0.68.0_x86\poppler-0.68.0\bin')




    tamanho = len(images)
    print("tamanho arquivo images ::", tamanho)
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


        width, height = im.size
        print("width, height -->", width, height)

        # Medição do Retangulo
        left = 1200
        top = 400
        right = 3000
        bottom = 560

        imRetangulo = im.crop((left, top, right, bottom))

        imRetangulo.save(fnameRetangulo,"PNG")

        text = str(((pytesseract.image_to_string(Image.open(fnameRetangulo)))))
        text1 = text.splitlines()  
        print("conteudo de text1 ===>", text1)

        print("remove retangulo")
        os.remove(fnameRetangulo)
        

        if "PRE-LISTA DE POSTAGEM - PLP" in text1 :
            print("achei a pre-lista de POSTAGEM")
            print("remove arquivo :", fname)
            print("conteudo de text1 ===>", text1)
            os.remove(fname)
            break
        else:
            print("não achei a Declaração")
            print("conteudo de text1 ===>", text1)
        



        ###############
        # Etiqueta 1
        ###############
        medidas = [220,200,1990,3123]
        medidas1 = [860,805,1380,870]
        print("# Etiqueta 1")
        print("medidas :", medidas)
        print("medidas1 :", medidas1)

        testar = processa_imagem(medidas, im, medidas1)

    
        print("testar :", testar)

        if(testar is not None):
            print("testar is not None")
            gerador = gerarArquivos(testar)
        print("Fim etiqueta 1...")

        
        ###############
        # Etiqueta 2
        ###############
        # medidas da segunda etiqueta, a4 , lado esquerdo, canto inferior
        
        medidas = [2050,200,3830,3123]
        medidas1 = [2700,805,3200,870]
        print(" Etiqueta 2")
        print("medidas :", medidas)
        print("medidas1 :", medidas1)

        testar = processa_imagem(medidas, im, medidas1)

        print("testar :", testar)
        
        if(testar is not None):
            print("testar is not None")
            gerador = gerarArquivos(testar)

        print("Fim etiqueta 2...")
        

        ###############
        # Etiqueta 3
        ###############
        # medidas da terceira etiqueta, a4 , lado direito, canto superior
        
        #medidas = [3890,720,5670,820]
        #print("medidas :", medidas)
        #medidas1 = [3890,990,5670,3910]
        #print("medidas :", medidas1)
        medidas = [3890,200,5670,3123]
        medidas1 = [4520,805,5040,870]
        print("# Etiqueta 3")
        print("medidas :", medidas)
        print("medidas :", medidas1)

        testar = processa_imagem(medidas, im, medidas1)

        print("testar :", testar)

        if(testar is not None):
            print("testar is not None")
            gerador = gerarArquivos(testar)
        
        """
        ###############
        # Etiqueta 4
        ###############
        # medidas da quarta etiqueta, a4 , lado direito, canto inferior
        
        #medidas = [2067,2921, 4132,5840]
        #print("medidas :", medidas)
        testar = processa_imagem(medidas, im)
        print("testar :", testar)
        if(testar is not None):
            print("testar is not None")
            gerador = gerarArquivos(testar)
        """


        print("remover o file : ", fname)
        print("Fim etiqueta 3...")
        #exit(98)

    #! os.remove(fname)
    
    return()
    
#ml_etiquetas_ml_2.pdf
#z = lerEtiquetas_ml("xml/ml_etiquetas_ml_1.pdf")
#! z = lerEtiquetas_ml("xml/ml_etiquetas_5_full.pdf")
#ml_etiquetas_1_05-10-2022