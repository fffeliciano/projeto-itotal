from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from uploadnf import views


urlpatterns = [
    #path('', views.notasList, name='notas-list'),
    
    #menu início
    #path('', views.home, name='home'),


    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

    #menu Home
    path( '', views.Home, name='home'),
    
    #path('home/'.secret_page, name='secret-page'),
    
    #path('', views.secret_page, name='secret-page'),
    #menu Upload
    #path('upload/', views.upload, name='upload'),
    
    #menu Produto
    path('material/', views.Produto, name='material'),
    path('prodhtml/', views.Produto_html, name='produto-html'),

    path('prod/<slug:codprod>', views.enviarProduto, name='prod_view'),
    path('editprod/<slug:codprod>', views.editProd, name='edit-prod'),
    path('delprod/<slug:codprod>', views.delProd, name='del-prod'),
    path('newprod/', views.newprod, name='new-prod'),
    path('extprod/<slug:codprod>', views.extprod, name="extprod"),


    # Lista do Estoque de produtos
    path('estoqueLog/', views.estoqueLog, name='estoqueLog'),
    #path('estoqueLog/<int:id>/', views.estoqueLog_envia, name='estoqueLog'),
    #path('separar/<int:numpedcli>/', views.separar_enviar, name='separar'),


    # Lista de Embarques
    path('embarque/', views.embarque, name='embarque'),
    




    #menu Fornecedor
    #path('suprimentos/', views.Fornecedor, name='suprimentos'),
    path('upload/', views.upload, name='upload'),
    path('nf/', views.nf, name='nf'),
    path('nf/<int:id>/', views.nf_exporta, name='nf_exporta'),

    #Menu Pedidos
    path('pdd/', views.pdd, name='pdd'),
    path('pdd/<int:numpedcli>/', views.pdd_exporta, name='pdd_exporta'),

    # Cancelar Pedido
    #path('pnf/', views.pnf, name='pnf'),
    path('pnfcancel/<int:numpedcli>/', views.pnf_cancela, name='pnf_cancela'),


    # Pedidos - Notas Fiscais
    path('nota/', views.nota, name='nota'),
    #path('nota/<int:numpedcli>/', views.nota_exporta, name='nota_exporta'),

    # Exporta os dados da Nota Fiscal, pegando informações do db de Notas fiscais.
    #path('pnf/', views.pdd, name='pdd'),
    path('pnf/<int:numpedcli>/', views.pnf_exporta, name='pnf_exporta'),

    # Separação de pedidos
    # Lista dos produtos Separados.
    path('separar/', views.separar, name='separar'),
    #path('separar/<int:numpedcli>/', views.separar_enviar, name='separar'),


   
    
  



    # Outros
    path('tfaa/', views.tfaa, name='tfaa'),
    path('tfaa/<int:id>/update/', views.tfaa_update, name='tfaa_update'),
    path('fornhtml/', views.Fornecedor_html, name='fornecedor-html'),



    path("external", views.external_api_view, name="external"),

    #path('nota/<int:id>', views.notaView, name='nota-view'),
    
    #path('notas/', views.notas, name='notas'),
    #path('extprod/<int:codprod>', views.extprod, name="extprod"),
    #path('prod/<int:codprod>', views.prodView, name='prod_view'),

    
    # path("external_nf/", views.external_nf, name="external_nf"),
    # path('notaenv/<int:nNF>', view. , name "enviar-nota"),
    #path('prod/<int:codprod>', views.enviarProduto, name='enviar-produto'),
    #path('posts/', views.posts, name='posts'),
    #path('sku/<int:id>', views.sku, name='sku'),
    #path('admin/', admin.site.urls),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




