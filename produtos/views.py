from produtos.models import Produtos, Embalagens
from produtos.serializers import ProdutosSerializer, EmbalagensSerializer
from rest_framework import viewsets
from url_filter.integrations.drf import DjangoFilterBackend


class ProdutosApiView(viewsets.ModelViewSet):
    queryset=Produtos.objects.all()
    serializer_class = ProdutosSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['codprod', 'updated_at']


class EmbalagensApiView(viewsets.ModelViewSet):
    queryset=Embalagens.objects.all()
    serializer_class = EmbalagensSerializer



    
