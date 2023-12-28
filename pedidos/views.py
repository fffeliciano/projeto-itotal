from pedidos.models import Pedidos, Itens, Embarque ,NotasFiscaisSaida, ItensNF
#from pedidos.models import Pedidos, Itens, NotasFiscaisSaida, ItensNF, EmbarqueFour

from pedidos.serializers import PedidosSerializer, ItensSerializer, EmbarqueSerializer, NotasFiscaisSaidaSerializer, ItensNFSerializer
#from pedidos.serializers import PedidosSerializer, ItensSerializer, NotasFiscaisSaidaSerializer, ItensNFSerializer, EmbarqueFourSerializer

from rest_framework import viewsets
from url_filter.integrations.drf import DjangoFilterBackend

import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse

from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes


class PedidosApiView(viewsets.ModelViewSet):
    queryset=Pedidos.objects.all()
    serializer_class = PedidosSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['updated_at', 'status']


class ItensApiView(viewsets.ModelViewSet):
    queryset=Itens.objects.all()
    serializer_class = ItensSerializer


class EmbarqueApiView(viewsets.ModelViewSet):
    queryset=Embarque.objects.all()
    serializer_class = PedidosSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['updated_at']
"""
class EmbarqueFourApiView(viewsets.ModelViewSet):
    queryset=EmbarqueFour.objects.all()
    serializer_class = PedidosSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['updated_at']
"""

class NotasFiscaisSaidaApiView(viewsets.ModelViewSet):
    queryset=NotasFiscaisSaida.objects.all()
    serializer_class = NotasFiscaisSaidaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['updated_at', 'status']


class ItensNFApiView(viewsets.ModelViewSet):
    queryset= ItensNF.objects.all()
    serializer_class = ItensNFSerializer
"""
class EtiquetasApiView(viewsets.ModelViewSet):
    queryset=Etiquetas.objects.all()
    serializer_class = EtiquetasSerializer
"""

@api_view(['POST', 'DELETE'])
@authentication_classes([])
@permission_classes([])

@csrf_exempt

def embarque_api(request):

    if (request.method == 'POST'):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serializer = EmbarqueSerializer(data=python_data['CORPEM_WMS_CONF_EMB'])

        if  serializer.is_valid():
            serializer.save()
            res = {'CORPEM_WS_OK': 'OK'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        return HttpResponse(JSONRenderer().render(serializer.errors), content_type='application/json')


""" if (request.method == 'DELETE'):
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
        """

"""
@api_view(['POST', 'DELETE'])
@authentication_classes([])
@permission_classes([])

@csrf_exempt
def embarqueFour_api(request):

    if (request.method == 'POST'):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serializer = EmbarqueFourSerializer(data=python_data['CORPEM_WMS_CONF_EMB'])

        if  serializer.is_valid():
            serializer.save()
            res = {'CORPEM_WS_OK': 'OK'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        return HttpResponse(JSONRenderer().render(serializer.errors), content_type='application/json')
    """
