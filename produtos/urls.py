from rest_framework.routers import DefaultRouter

from produtos.views import ProdutosApiView, EmbalagensApiView

router = DefaultRouter()
router.register(r'', ProdutosApiView, basename='produtos')


produtos_urls = router.urls

