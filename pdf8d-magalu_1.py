from pdf2image import convert_from_path
from PIL import Image 

import pytesseract
import sys
import os
import re

#from pathlib import Path

from datetime import date 


import zpl 
import pickle

#! Incluir linha abaixo ( no Ubunto não deve precisar, pois temos um path do pytesseract)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def processa_imagem(medidas, im):

    imRt = im.crop((medidas))
    #ubuntu
    fileNameImg = './etiquetas/nameImagem.png'
    #fileNameImg = 'etiquetas/nameImagem.png'

    imRt.save(fileNameImg,"PNG")

    #exit(80)
    
    text = str(((pytesseract.image_to_string(Image.open(fileNameImg)))))
    texto = text.splitlines()
    new_teste = text.split('\n')
    print("texto ------>", texto)

    for i in new_teste :
        print("valor de i -->",i)









    
    if not texto :
        print("Vazio")
        # Deletar aqui os arquivos que não vou mais utilizar
        # nameImagem.png
        print("remove")
        os.remove(fileNameImg)
    else:
        print("Tem Conteúdo, segue o jogo")

        """
        select_elements1 = [texto[index] for index in indices]

        

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
            
            print(newName1 + ".txt")
            print(len(newName1))
            # os.remove(fileName1)
            
            os.rename(fileNameImg, newName1 + ".png")


            return(newName3  )
        """
        localizar_nt = re.compile(".*04268-020")
        print("--- localizar_nt --->", localizar_nt)

        
        filtered_list3 = list(filter(localizar_nt.match, new_teste ))
        print("--- filtered_list3 --->", filtered_list3)
        r_filtered_list3 = ''.join(filtered_list3)
        print("--- r_filtered_list3 --->", r_filtered_list3)
        localiza3 = new_teste.index(r_filtered_list3)
        print("--- localiza3 --->", localiza3 )
        nfstr = new_teste[localiza3]
        print("--- nfstr   >", nfstr)
        

        nomeArquivo = str(int(nfstr[9:16]))
        img_nameFile = str(int(nfstr[9:16]))+'.png'

        print("--- str(int(nfstr[9:16])) --->", str(int(nfstr[9:16])))
        print("--- img_nameFile --->", img_nameFile)
        
        #print("--- str(int(nfstr[9:16])) --->", str(int(nfstr[:-6])))
        #print("--- img_nameFile --->", img_nameFile)

        text_nameFile = str(int(nfstr[9:16]))+ "-dadosetq" + '.txt'
        print("--- text_nameFile --->", text_nameFile)

        #with open( "./etiquetas/" + text_nameFile , 'wb' ) as temp:
        #    print("Vou salvar arquivo dados da etiqueta")
        #    pickle.dump(new_teste, temp)

        return(nomeArquivo)




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


    fileName2 = f'C:\\ProgramData\\anaconda3\\envs\\projeto-es\\etiquetas\\{nrNota}.png'
    print("*** fileName2 : ", fileName2)


    #C:\Users\Fernando\anaconda3\envs\projeto-es\

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

    path = 'C:\\ProgramData\\anaconda3\\envs\\projeto-es'

    #print("conteúdo do fileName2", fileName2)

    print("fileName2 --linha 171 --->>", fileName2)
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


    teste = pytesseract.image_to_string( Image.open("./etiquetas/" + fileName1) )
    new_teste = teste.split('\n')
    print(new_teste)

    #exit(88)

    with open( f'./etiquetas/{nrNota}-dadosetq.txt' , 'wb' ) as temp:
        print("Vou salvar arquivo dados da etiqueta")
        pickle.dump(new_teste, temp)


    return




#-------------------------------------------------------------------------------------------------------------

print("começou ...")

# shopee-23-03-2022
# images = convert_from_path("xml/shopee-23-03-2022.pdf", 500,poppler_path=r'C:\Program Files (x86)\poppler\poppler-0.68.0_x86\poppler-0.68.0\bin')

#images = convert_from_path("xml/magalu-5.pdf", 500,poppler_path=r'C:\Program Files (x86)\poppler\poppler-0.68.0_x86\poppler-0.68.0\bin')
images = convert_from_path("xml/magalu-5.pdf", 500,poppler_path=r'C:\Program Files\poppler-0.67.0_x86\poppler-0.67.0\bin')
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



    # Definindo o nome dos arquivos
    print("3)valor de i :", i)
    fname = 'etiquetas\\image'+str(i)+'.png'
    fname1 = 'etiquetas\\image'+str(i)+'.png'
    fnameRetangulo = 'etiquetas\\image-retangulo'+str(i)+'.png'
    

    
    #image.save(fname, "PNG")
    print("criando o arquivo :", fname)
    image.save(fname, "PNG")

    #exit(90)
    #print(fname, fname2, fname3)
    
    # Criar um if abaixo, e avaliar um retangulo se tem o texto "Declaração"
    # se tiver Declaração rodar com o "continue"


    # Opens a image in RGB mode
    im = Image.open(f"C:\\ProgramData\\anaconda3\\envs\\projeto-es\\{fname}")
    #im = Image.open(f"/home/ubuntu/projeto-es/{fname1}")

    print("1)valor de ", i)
    #if i > tamanho - 3 :
    #    print("2)valor de ", i)
    #    continue


    

    #arquivo_upload = 'shopee-26-03-2022.pdf'
    #print("Arquivo extenção = ", arquivo_upload.suffix)
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)


    """
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

    




    # Setting the points for cropped image
    #left = 5
    #top = height / 4
    #right = 164
    #bottom = 3 * height / 4
    

    indices = [1,2,3,4,5]
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


        #exit(90)
    """


    # Etiqueta 1
    # medidas da primeira etiqueta, a4 , lado esquerdo, canto superior
    medidas = [0,0,2066,2920]
    print("medidas :", medidas)

    testar = processa_imagem(medidas, im)

    print("testar :", testar)


    if(testar is not None):
        print("testar is not None")
        gerador = gerarArquivos(testar)


    


    # Etiqueta 2
    # medidas da segunda etiqueta, a4 , lado esquerdo, canto inferior
    medidas = [0,2921,2066,5840]
    print("medidas :", medidas)

    testar = processa_imagem(medidas, im)

    print("testar :", testar)
    
    if(testar is not None):
        print("testar is not None")
        gerador = gerarArquivos(testar)




    # Etiqueta 3
    # medidas da terceira etiqueta, a4 , lado direito, canto superior
    medidas = [2067,0,4132,2920]
    print("medidas :", medidas)

    testar = processa_imagem(medidas, im)

    print("testar :", testar)

    if(testar is not None):
        print("testar is not None")
        gerador = gerarArquivos(testar)



    # Etiqueta 4
    # medidas da quarta etiqueta, a4 , lado direito, canto inferior
    medidas = [2067,2921, 4132,5840]
    print("medidas :", medidas)

    testar = processa_imagem(medidas, im)

    print("testar :", testar)

    if(testar is not None):
        print("testar is not None")
        gerador = gerarArquivos(testar)



    print("remover o file : ", fname)
