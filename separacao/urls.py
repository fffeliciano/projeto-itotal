from rest_framework.routers import DefaultRouter
from rest_framework import routers

from separacao.views import SeparacaoView, ItensSeparacaoView

#, RetornoItensNFEntradaView, RetItensListView, RetItensView, retorno_api
from separacao import views


from django.urls import path, include

from django.conf import settings


#---------------------------------------------------------

#router = DefaultRouter()
#router.register(r'notasfiscais/', NotasFiscaisApiView, basename='notas-fiscais')

#separacao_urls = router.urls

#router = DefaultRouter()
        #router.register(r'notasfiscais', NotasFiscaisApiView, basename='nfe')
#router.register(r'separacao', SeparacaoView, basename='separacao-view')



#----------------------------------------------------------

#router = routers.SimpleRouter()




urlpatterns = [

#url(r'nfe/', NotasFiscaisApiView),
#url(r'sku/', SkuApiView),

    #path(r'tfaa1/', RetornoItensNFEntradaListView.as_view(), name='tfaa1'),
    #path(r'tfaa1/<int:ChaveNF>', RetornoItensNFEntradaView.as_view(), name='tfaa2'),
    #path(r'tfaa/<int:id>', RetornoItensNFEntradaView.as_view(), name='tfaa2'),
    #path(r'retnf/', RetItensListView.as_view(), name='retnf1'),
    #path(r'retnf/<int:id>', RetItensView.as_view(), name='retnf2'),
    #path(r'', views.SeparacaoView, name='sep'),
    path(r'separacao_api/', views.separacao_api, name='separacao-api')
    #router.register(r'separacao', SeparacaoView, basename='separacao-view')

    
]



#fornecedor_urls = router.urls

#url(r'retorno', views.retorno_details, basename='retorno-view')

#urlpatterns = [
    #path('', views.notasList, name='notas-list'),
#    path('new', views.retorno_details, name='retorno-view')
#]


#urlpatterns += router.urls



#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


