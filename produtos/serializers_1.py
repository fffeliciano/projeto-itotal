



from .models import Produtos, Embalagens
from rest_framework import serializers

class EmbalagensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Embalagens
        fields = '__all__'

class ProdutosSerializer(serializers.ModelSerializer):
    #disponivel = serializers.ReadOnlyField()
    #embalagens = EmbalagensSerializer()

    class Meta:
        model = Produtos
        #fields = '__all__'
        exclude = []




        