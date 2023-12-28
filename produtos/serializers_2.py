



from .models import Produtos, Embalagens
from rest_framework import serializers

class ProdutosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtos
        fields = '__all__'

class EmbalagensSerializer(serializers.ModelSerializer):
    #disponivel = serializers.ReadOnlyField()
    produtos = ProdutosSerializer()

    class Meta:
        model = Embalagens
        fields = '__all__'
        #exclude = []