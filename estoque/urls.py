from rest_framework.routers import DefaultRouter

from estoque.views import EstoqueApiView, ItensApiView

router = DefaultRouter()
router.register(r'', EstoqueApiView, basename='estoque')

estoque_urls = router.urls
