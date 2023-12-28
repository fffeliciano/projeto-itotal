from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index')
] 



from rest_framework.routers import DefaultRouter

from .views import ProdutosViewSet

router = DefaultRouter()
#router.register(r'', ProdutosViewSet, basename='produtos')
router.register(r'', ProdutosViewSet, basename='produtos')

produtos_urls = router.urls