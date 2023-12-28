import PyPDF2

with open('xml/shopee-24-06-2022-1_Y4oTGwG.pdf', 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    
    
    print(f'Number of Pages in PDF File is {pdf_reader.getNumPages()}')
    print(f'PDF Metadata is {pdf_reader.documentInfo}')
    #print(f'PDF File Author is {pdf_reader.documentInfo["/Author"]}')
    #print(f'PDF File Creator is {pdf_reader.documentInfo["/Creator"]}')



print("fim..")
