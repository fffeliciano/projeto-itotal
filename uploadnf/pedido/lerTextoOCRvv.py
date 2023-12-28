#import codecs

# Ubuntu
# Trocar path abaixo:
# ".\\etiquetas\\"
# por 
#'./etiquetas/'




#from pdf2image import convert_from_path


from PIL import Image # Importando o módulo Pillow para abrir a imagem no script
import pytesseract # Módulo para a utilização da tecnologia OCR
import re
import os

import pickle
from pedidos.models import Pedidos
import platform


#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#pytesseract.pytesseract.tesseract_cmd = r'/usr/share/tesseract-ocr/4.00/tessdata'
def lerTexto(fileImg):
    
    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    else:
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

    



    #print("Name File recebido (fileImg) ", fileImg)

    if platform.system()=='Windows':
        pathFile = '.\\etiquetas\\' + fileImg
    else:
        pathFile = './etiquetas/' + fileImg
    

    #path = os.getcwd()
    #print("--- pathFile --->", pathFile )
    #exit(99)
    
    teste = pytesseract.image_to_string( Image.open(pathFile) )
    new_teste = teste.split('\n')

    

    #print(new_teste)
    #print(type(new_teste))


    localizar_nt = re.compile(".*Nota:")
    #print("--- localizar_nt --->", localizar_nt)
    filtered_list3 = list(filter(localizar_nt.match, new_teste ))
    #print("--- filtered_list3 --->", filtered_list3)
    
    
    if filtered_list3 == []:
        print("vazio, não achei a Nota")

        
        localizar_nt = re.compile(".*Pedido:")
        print("--- localizar_Pedido --->", localizar_nt)
        filtered_list3 = list(filter(localizar_nt.match, new_teste ))
        print("--- filtered_list3 Pedido--->", filtered_list3)
        pddstr = filtered_list3[0][8:20]
        print("Numero do pedido pddstr ===>, tamanho", pddstr.strip(), len(pddstr.strip()))
        nrPdd = pddstr.strip()

        

        w = Pedidos.objects.filter(numpedrca = nrPdd.replace(" ", "")+"|envvias").values('numnf')
        

        

        print('número da Nota Fiscal',w)
        y = w[0]
        print("y ===> :", y)
        print("y ===>", y['numnf'])

        #exit(88)


        nr_nota = y['numnf']


    else:
        print("cheio,  achei a Nota")

        
        r_filtered_list3 = ''.join(filtered_list3)
        print("--- r_filtered_list3 --->", r_filtered_list3)
        localiza3 = new_teste.index(r_filtered_list3)
        print("--- localiza3 --->", localiza3 )
        nfstr = new_teste[localiza3]
        print("--- nfstr   >", nfstr)
        nr_nota = nfstr[9:16]
    

    #exit(90)




    img_nameFile = str(int(nr_nota))+'.png'

    print("--- str(int(nfstr[9:16])) --->", str(int(nr_nota)))
    print("--- img_nameFile --->", img_nameFile)

    text_nameFile = str(int(nr_nota))+ "-dadosetq" + '.txt'
    print("--- text_nameFile --->", text_nameFile)

    #with open( text_nameFile , 'w', encoding='UTF-8') as f:
    #    print("Vou salvar arquivo dados da etiqueta")
    #    f.write(new_teste)

    

    with open( "./etiquetas/" + text_nameFile , 'wb' ) as temp:
        print("Vou salvar arquivo dados da etiqueta")
        pickle.dump(new_teste, temp)

    #           IMPORTANTE  Quando quizer Ler o conteúdo do arquivo acima.
    #with open (text_nameFile, 'rb') as temp:
    #    items = pickle.load(temp)
    #print(items)





    

    print('Via Varejo')
    print("Nota Numero :",nr_nota)
    print("--- nome arquivo ---", str(int(nr_nota))+".pdf" )
    
    
    cwd = os.getcwd()
    #print("--- cwd --->", cwd)
    #cwd1 = cwd + '\etiquetas\\'
    #print("--- cwd1 --->", cwd1 )

    
    
    #newName_file = os.path.join(cwd1, text_nameFile)
    #print("--- newName_file --->", newName_file)

    #fileImg[:-4] + "txt"
    



    # Verificar o diretório e o arquivo no Ubuntu se está ok
    #remove_file = os.path.join(cwd, fileImg)
    #print("--- remove_file --->", remove_file)
    #os.remove(remove_file)



    # Rename no arquivo ZPL.txt 
    #source_file = os.path.join(cwd, fileImg[:-4] + ".zpl")
    #print("--- source_file --->", source_file)
    
    #zpl_nameFile = str(int(nfstr[9:16]))+'.zpl'
    #new_zpl_nameFile = os.path.join(cwd, zpl_nameFile)
    
    #print("--- new_zpl_nameFile --->", new_zpl_nameFile)
    
    
    #os.rename( source_file , new_zpl_nameFile)
    #os.replace( source_file , new_zpl_nameFile)

    
    
    print("Travado!!!")
    #exit(88)

    return(str(int(nr_nota)))
