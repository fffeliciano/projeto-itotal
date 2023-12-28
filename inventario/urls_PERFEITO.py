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
from nfentrada.urls import nfentrada_urls
from retnfentrada.urls import retnfentrada_urls

#from Produtos.views import produtos_view
#from produtos_view.views import ProdutosApiView, EmbalagensApiView

#from nfentrada.views import PedidosEntradaApiView, ItensEntradaSerializer
#from retnfentrada.views import RetornoNFEntradaApiView, ItensNFEntradaApiView

urlpatterns = [
    #path('', admin.site.urls),
    path('admin/', admin.site.urls),
    path('produtos/', include(produtos_urls)),
    path('nfentrada/', include(nfentrada_urls)),
    path('retnfentrada/', include(retnfentrada_urls)),
 ]
