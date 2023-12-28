nrEtiqueta = input("Digite o numero da Nota Fiscal: ")

with open( f'etiquetas/{nrEtiqueta}.txt', 'w') as f:
    f.write("0")
