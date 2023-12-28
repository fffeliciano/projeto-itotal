from produtos.models import Produtos, Embalagens
from produtos.serializers import ProdutosSerializer, EmbalagensSerializer
from rest_framework import viewsets

class ProdutosApiView(viewsets.ModelViewSet):
    queryset=Produtos.objects.all()
    serializer_class = ProdutosSerializer


class EmbalagensApiView(viewsets.ModelViewSet):
    queryset=Embalagens.objects.all()
    serializer_class = EmbalagensSerializer

