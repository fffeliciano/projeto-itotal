from django.shortcuts import render

# Create your views here.





#------------------------------------------------------

from separacao.models import Separacao, ItensSeparacao
from separacao.serializers import SeparacaoSerializer, ItensSeparacaoSerializer
from rest_framework import viewsets
from url_filter.integrations.drf import DjangoFilterBackend

from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse

from rest_framework import generics
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.http import require_http_methods
from rest_framework import status

from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes

# Separacao
class SeparacaoListView(generics.ListCreateAPIView):
    queryset= Separacao.objects.all()
    serializer_class = SeparacaoSerializer

class SeparacaoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SeparacaoSerializer
    queryset = Separacao.objects.all()
    

# ItensSeparacao
class ItensSeparacaoListView(generics.ListCreateAPIView):
    queryset = ItensSeparacao.objects.all()
    serializer_class = ItensSeparacaoSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['updated_at']

class ItensSeparacaoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItensSeparacaoSerializer
    queryset = ItensSeparacao.objects.all()





@api_view(['POST'])
@authentication_classes([])
@permission_classes([])

@csrf_exempt
def separacao_api(request):

    if (request.method == 'POST'):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serializer = SeparacaoSerializer(data=python_data['CORPEM_WMS_CONF_SEP'])

        if  serializer.is_valid():
            serializer.save()
            res = {'CORPEM_WS_OK': 'OK'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        return HttpResponse(JSONRenderer().render(serializer.errors), content_type='application/json')
        
    elif (request.method == 'DELETE'):


    #if (request.method == 'DELETE'):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id')
        if id is not None:
            try:
                nf = Separacao.objects.get(id=id)
            except Separacao.DoesNotExist:
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
    
    else:
        return render(request, 'separacao/')
        #return render(request, '././pedidos/')


'''
@csrf_exempt
def retorno_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serializer = SeparacaoSerializer(data=python_data)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Created Successfully'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        return HttpResonse(JSONRenderer().render(serializer.errors), content_type='application/json')
'''

@csrf_exempt
def retorno(request):
    nf = Separacao.objects.get(id=42)
    serailizer = SeparacaoSerializer(nf)
    print(serailizer.data)
    json_data = JSONRenderer().render(serailizer.data)
    return HttpResponse(json_data, content_type='application/json')


