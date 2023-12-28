from estoque.models import Estoque, Itens
from estoque.serializers import EstoqueSerializer, ItensSerializer
from rest_framework import viewsets

from url_filter.integrations.drf import DjangoFilterBackend

class EstoqueApiView(viewsets.ModelViewSet):
    queryset=Estoque.objects.all()
    serializer_class = EstoqueSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['updated_at']

class ItensApiView(viewsets.ModelViewSet):
    queryset=Itens.objects.all()
    serializer_class = ItensSerializer

