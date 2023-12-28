from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from uploadnf import views


'''
urlpatterns = [
    path('uploadnf/', HomeView.as_view()),
]'''

urlpatterns = [
    #path('', views.notasList, name='notas-list'),
    path('nota/<int:id>', views.notaView, name='nota-view'),
    path('home/', views.Home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('prodhtml/', views.Produto_html, name='produto-html'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('Fornecedor/', views.Fornecedor, name='fornecedor'),
    path('Produto/', views.Produto, name='produto'),
    #path('prod/<int:codprod>', views.prodView, name='prod_view'),
    path('prod/<int:codprod>', views.enviarProduto, name='prod_view'),
    path('newprod/', views.newprod, name='new-prod'),
    path('editprod/<int:codprod>', views.editProd, name='edit-prod'),
    path('delprod/<int:codprod>', views.delProd, name='del-prod'),
    
    path("extprod/<int:codprod>", views.extprod, name="extprod"),
    
    
    #path('prod/<int:codprod>', views.enviarProduto, name='enviar-produto'),
    #path('posts/', views.posts, name='posts'),
    #path('sku/<int:id>', views.sku, name='sku'),
    #path('admin/', admin.site.urls),
    path("external", views.external_api_view, name="external")
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




'''
urlpatterns = [
    path('uploadnf/', TemplateView.as_view(template_name="home.html")),
]'''