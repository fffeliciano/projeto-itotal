from pdf2image import convert_from_path

file = "shopee-22-03-2022-full.pdf"

images = convert_from_path(file)

tamanho = len(images)
print(tamanho)

for i, image in enumerate(images):
    fname = 'image88'+str(i)+'.png'
    fnameRetangulo = 'image-retangulo88'+str(i)+'.png'
    image.save(fname,"PNG")



