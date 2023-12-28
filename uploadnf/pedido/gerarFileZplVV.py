#import codecs

# Ubuntu
# Trocar path abaixo:
# ".\\etiquetas\\"
# por 
#'./etiquetas/'


from bs4 import BeautifulSoup
from io import BytesIO
import re, time, base64, os




#def getFromBase64(img_data, image_path="c:\\ProgramData\\Anaconda3\\envs\\projeto_es\\etiquetas\\"):
def getFromBase64(img_data, filename):




    print("--- filename arquivo recebido getFromBase64 --->", filename)

    print("type dados originais", type(img_data))
    
    #exit(90)
    #print("img_data", img_data)
    base1 = "'" + img_data + "'"
    print("base1 --->", type(base1))
    
    #with open( filename + '.txt', 'w') as f:
    #    print("Vou salvar arquivo")
    #    f.write(base1)

    #print("salvei...")
    #exit(90)
    


    
    #print(base1)
    #exit(90)
    base = base1.replace('data:image/png;base64,', '')

    print("consegui criar base ...")

    with open( "./etiquetas/" + filename + '.txt', 'w') as f:
        #print("Vou salvar arquivo" + "./etiquetas/" + filename + ".txt")
        f.write(base)



    imgdata = base64.b64decode(base)

    fileImg =  filename + '.png'  # I assume you have a way of picking unique filenames
    with open( "./etiquetas/" + fileImg, 'wb') as f:
        f.write(imgdata)


    #exit(90)
    os.remove( "./etiquetas/" + filename+".txt" )


    return(fileImg)







## **********************************************************************************************




#  print(l.dumpZPL())
#print(l.dumpZPL())
#l.preview()
