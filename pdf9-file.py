import os
arquivo, extensao = os.path.splitext('shopee-04-04-2022.pdf')
print(arquivo)

print(extensao)


if extensao == '.pdf':
    print("tratar aqui arquivo upload tipo PDF")
elif extensao == '.html':
    print('tratar aqui arquivo upload tipo html')
else:
    print("não identifiquei", extensao)