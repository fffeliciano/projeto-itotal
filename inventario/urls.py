"""inventario URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from produtos.urls import produtos_urls
#from separacao.urls import separacao_urls
#from pedidos.urls import pedidos_urls
from estoque.urls import estoque_urls
#from embarque.urls import embarque_urls
#from fornecedor.urls import fornecedor_urls
#from uploadnf.urls import path, inc
#from retnfentrada.urls import retnfentrada_urls

#from Produtos.views import produtos_view
#from produtos_view.views import ProdutosApiView, EmbalagensApiView

#from nfentrada.views import PedidosEntradaApiView, ItensEntradaSerializer
#from retnfentrada.views import RetornoNFEntradaApiView, ItensNFEntradaApiView

urlpatterns = [
    #path('', admin.site.urls),
    path('admin/', admin.site.urls),
    path('produtos/', include(produtos_urls)),
    
    path('estoque/', include(estoque_urls)),
    #path('embarque/', include(embarque_urls)),
    #path('fornecedor/', include(fornecedor_urls)),
    #path('pedidos/', include(pedidos_urls)),
    path('pedidos/', include('pedidos.urls')),
    path('fornecedor/', include('fornecedor.urls')),
    path('separacao/', include('separacao.urls')),
    path('', include('uploadnf.urls')),
 ]

#path('retnfentrada/', include(retnfentrada_urls)),