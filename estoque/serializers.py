from estoque.models import Estoque, Itens
from rest_framework import serializers


class ItensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itens
        fields = ('cd', 'ft', 'qc', 'qb', 'qf')
        #fields = ('numseq', 'codprod', 'qtprod', 'qtconf', 'lotfab', 'dtfab', 'dtven', 'vlr_unit')
 

 

class EstoqueSerializer(serializers.ModelSerializer):
      itens = ItensSerializer(many=True)
      class Meta:
        model = Estoque
        fields = ('id', 'nome_atualizacao' ,'created_at', 'updated_at', 'itens' )
        #fields = '__all__'

      def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        idestoque = Estoque.objects.create(**validated_data)
        for tr in itens_data:
            Itens.objects.create(idestoque=idestoque, **tr)
        return idestoque

      def update(self, instance, validated_data):
          itens_data = validated_data.pop('itens')
          items = (instance.itens).all()
          items = list(items)
          instance.nome_atualizacao = validated_data.get('nome_atualizacao', instance.nome_atualizacao)
          instance.save()

          for item_data in itens_data:
              itm = items.pop(0)
              itm.ft = item_data.get('ft',itm.ft)
              itm.qc = item_data.get('qc', itm.qc)
              itm.qb = item_data.get('qb', itm.qb)
              itm.qf = item_data.get('qf', itm.qf)
              itm.save()
          return instance


