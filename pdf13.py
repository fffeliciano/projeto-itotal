

import base64
import pdfkit

#path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
path_wkhtmltopdf = r"/usr/local/bin/wkhtmltopdf"


config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# pdfkit.from_url( 'https://google.com.br' , 'google.pdf' , configuration = config)

"""
with open('./teste4_files/americanas-entrega.png', 'rb') as binary_file:
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')


with open('./teste4_files/correios_m3_servico_express.png', 'rb') as binary_file:
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')


print(base64_message)

exit(90)
"""



pdfkit.from_file( 'teste6.html', 'etiquetas/teste4-1c.pdf', configuration = config)












"""
options = array(
                'encoding' => 'UTF-8',
                'margin-top' => 5,
                'margin-bottom' => 5,
                'dpi' => 120,
                'page-size': 'A4',
            );
"""

