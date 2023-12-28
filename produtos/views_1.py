from django.shortcuts import render
from django.http import HttpResponse



def index(request):
    return HttpResponse('<h1>Produtos</h1> <h2>Bem vindo!</h2> ')


from rest_framework import viewsets
from .serializers import ProdutosSerializer



from .models import Produtos

class ProdutosViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutosSerializer
    queryset = Produtos.objects.all()