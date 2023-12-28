#from rest_framework import api_view
from rest_framework.response import Response
#from django.http import HttpResponse
from rest_framework.views import APIView

from .serializers import ProdutosSerializer

from .models import Produtos

class ProdutosApiView(APIView):
    """
    Utilize este endereço para gerenciar seus produtos
    """
    def get(self, request):
        produtos = Produtos.objects.all()
        serializer = ProdutosSerializer(produtos, many=True)
        return Response(serializer.data)

produtos_view = ProdutosApiView.as_view()


