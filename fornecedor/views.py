from fornecedor.models import NotasFiscais, Itens, Sku, RetornoItensNFEntrada, RetItens
from fornecedor.serializers import NotasFiscaisSerializer, ItensSerializer, SkuSerializer, RetornoItensNFEntradaSerializer, RetItensSerializer
from rest_framework import viewsets
from url_filter.integrations.drf import DjangoFilterBackend

from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse

#from __future__ import unicode_literals
from rest_framework import generics
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


from django.views.decorators.http import require_http_methods
from rest_framework import status

from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes

class NotasFiscaisApiView(viewsets.ModelViewSet):
    queryset=NotasFiscais.objects.all()
    serializer_class = NotasFiscaisSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['nNF', 'updated_at', 'chNFe']


class ItensApiView(viewsets.ModelViewSet):
    queryset=Itens.objects.all()
    serializer_class = ItensSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['idnf', 'nItem', 'cProd']


class SkuApiView(viewsets.ModelViewSet):
    queryset=Sku.objects.all()
    serializer_class = SkuSerializer







class RetornoItensNFEntradaListView(generics.ListCreateAPIView):
    queryset= RetornoItensNFEntrada.objects.all()
    serializer_class = RetornoItensNFEntradaSerializer

class RetornoItensNFEntradaView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RetornoItensNFEntradaSerializer
    queryset = RetornoItensNFEntrada.objects.all()
    


class RetItensListView(generics.ListCreateAPIView):
    queryset = RetItens.objects.all()
    serializer_class = RetItensSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['updated_at']

class RetItensView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RetItensSerializer
    queryset = RetItens.objects.all()


@api_view(['POST', 'DELETE'])
@authentication_classes([])
@permission_classes([])
@csrf_exempt
def retorno_api(request):

    if (request.method == 'POST'):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serializer = RetornoItensNFEntradaSerializer(data=python_data['CORPEM_WMS_FECHA_DE'])

        if  serializer.is_valid():
            serializer.save()
            res = {'CORPEM_WS_OK': 'OK'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        return HttpResponse(JSONRenderer().render(serializer.errors), content_type='application/json')


    if (request.method == 'DELETE'):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        if id is not None:
            try:
                nf = RetornoItensNFEntrada.objects.get(id=id)
            except RetornoItensNFEntrada.DoesNotExist:
                res = {'msg':"id da chave de Nota Fiscal não exite"}
                json_data = JSONRenderer().render(res)
                return HttpResponse(Json_data, content_type='application/json')
            nf.delete()
            res = {'msg':"id de chave deletado com sucesso"}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type="application/json")
        res = {'msg': "Confira id da chave da Nota Fiscal"}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')


'''
@csrf_exempt
def retorno_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serializer = RetornoItensNFEntradaSerializer(data=python_data)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Created Successfully'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        return HttpResonse(JSONRenderer().render(serializer.errors), content_type='application/json')
'''

@csrf_exempt
def retorno(request):
    nf = RetornoItensNFEntrada.objects.get(id=42)
    serailizer = RetornoItensNFEntradaSerializer(nf)
    print(serailizer.data)
    json_data = JSONRenderer().render(serailizer.data)
    return HttpResponse(json_data, content_type='application/json')












