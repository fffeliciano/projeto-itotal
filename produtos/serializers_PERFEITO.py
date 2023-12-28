from produtos.models import Produtos, Embalagens
from rest_framework import serializers


class EmbalagensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Embalagens
        #fields = ('codunid', 'fator', 'codbarra', 'pesoliq', 'pesobru', 'alt', 'lar', 'comp', 'vol')
                 
        fields = '__all__'
        #exclude  = ['id']
        

 
class ProdutosSerializer(serializers.ModelSerializer):
    #embalagens = EmbalagensSerializer(many=True, read_only=True)
    embalagens = EmbalagensSerializer(many=True)
    class Meta:
        model = Produtos
        #fields = ('nomeprod', 'codprod', 'iws_erp', 'tpolret', 'iautodtven', 'qtddpzoven', 'ilotfab', 'idtfab', 'idtven', 'inser', 'codfab', 'nomefab', 'status', 'embalagens')
        fields = '__all__'




    def create(self, validated_data):
        embalagens_data = validated_data.pop('embalagens')
        produtos = Produtos.objects.create(**validated_data)
        for tr in embalagens_data:
            Embalagens.objects.create(produtos=produtos, **tr)
        return produtos

    def update(self, instance, validated_data):
        embalagens_data = validated_data.pop('embalagens')
        embs = (instance.embalagens).all()
        embs = list(embs)
        instance.iws_erp = validated_data.get('iws_erp', instance.iws_erp)
        instance.tpolret = validated_data.get('tpolret', instance.tpolret)
        instance.iautodtven = validated_data.get('iautodtven', instance.iautodtven)
        instance.qtddpzoven = validated_data.get('qtddpzoven', instance.qtddpzoven)
        instance.ilotfab = validated_data.get('ilotfab', instance.ilotfab)
        instance.idtfab = validated_data.get('idtfab', instance.idtfab)
        instance.idtven = validated_data.get('idtven', instance.idtven)
        instance.inser = validated_data.get('inser', instance.inser)
        instance.codfab = validated_data.get('codfab', instance.codfab)
        instance.nomefab = validated_data.get('nomefab', instance.nomefab)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        for embalagem_data in embalagens_data:
            emb = embs.pop(0)
            emb.codunid = embalagem_data.get('codunid',emb.codunid)
            emb.fator = embalagem_data.get('fator', emb.fator)
            emb.codbarra = embalagem_data.get('codbarra', emb.codbarra)
            emb.pesoliq = embalagem_data.get('pesoliq', emb.pesoliq)
            emb.pesobru = embalagem_data.get('pesobru', emb.pesobru)
            emb.alt = embalagem_data.get('alt', emb.alt)
            emb.lar = embalagem_data.get('lar', emb.lar)
            emb.comp = embalagem_data.get('comp', emb.comp)
            emb.vol = embalagem_data.get('vol', emb.vol)
            emb.save()
        return instance



            


