import imgkit


#path_wkhtmltoimage = r"/usr/local/bin/wkhtmltoimage"




#imgkit.from_file('teste5d.html' , 'html5d.png' )




#imgkit.from_url('http://google.com', 'out.png', options=options, )

path_wkthmltoimage = r'/usr/local/bin/wkhtmltoimage'

config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)


imgkit.from_file('teste5d.html', 'teste5d.jpg',config=config)

