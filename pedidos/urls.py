from rest_framework.routers import DefaultRouter

from pedidos.views import PedidosApiView, ItensApiView, EmbarqueApiView, NotasFiscaisSaidaApiView, ItensNFApiView
#from pedidos.views import PedidosApiView, ItensApiView, NotasFiscaisSaidaApiView, ItensNFApiView, EmbarqueFourApiView

from django.urls import path, include
from pedidos import views





router = DefaultRouter()
router.register(r'pedidos', PedidosApiView, basename='pedidos')
router.register(r'pedidos/<int:numpedcli>/$', PedidosApiView, basename='pedidosup')
#router.register(r'etiquetas', EtiquetasApiView, basename='etiquetas')

router.register(r'notasfiscais', NotasFiscaisSaidaApiView, basename='notasFiscaisSaida')


urlpatterns = [
    path(r'embarque_api/', views.embarque_api, name='embarque'),
    #path(r'embarqueFour_api/', views.embarqueFour_api, name='embarqueFour'),
]




urlpatterns += router.urls
#pedidos_urls += router.urls
