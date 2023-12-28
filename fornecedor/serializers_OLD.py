from fornecedor.models import NotasFiscais, Itens, Sku, RetornoItensNFEntrada
from rest_framework import serializers

from rest_framework.validators import UniqueTogetherValidator


class RetornoItensNFEntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetornoItensNFEntrada
        #fields = ('numseq', 'codprod', 'qtprod', 'qtavaria', 'qtfalta', 'lotfab', 'dtfab', 'dtven', 'chave_nfe')
        fields = '__all__' 







class ItensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itens
        fields = ( 'nItem', 'cProd', 'cEAN', 'xProd', 'NCM', 'CFOP', 'uCom', 'qCom', 'vUnCom', 'vProd', 'cEANTrib','uTrib', 'qTrib', 'vUnTrib', 'indTot', 'ean', 'nsku')
        #fields = ('cProd', 'cEAN', 'xProd', 'NCM', 'CFOP', 'uCom', 'qCom', 'vUnCom', 'vProd', 'cEANTrib','uTrib', 'qTrib', 'vUnTrib', 'indTot', 'ean')
                   
        #fields = '__all__'
        #exclude  = ['id']
         

 
class NotasFiscaisSerializer(serializers.ModelSerializer):
    #embalagens = ItensSerializer(many=True, read_only=True)
    itens = ItensSerializer(many=True)
  #  tfaa = RetornoItensNFEntradaSerializer(many=True)
    class Meta:
        model = NotasFiscais
        fields = ('chNFe', 'natOp', 'serie', 'nNF', 'dhEmi', 'CNPJ_emit', 'xNome_emit', 'vBC', 'vICMS', 'vProd', 'vFrete', 'vSeg', 'vDesc', 'vII', 'vIPI', 'vIPIDevol', 'vPIS', 'vCOFINS', 'vOutro', 'vNF', 'CNPJ_dest', 'xNome_dest', 'ws_tpdestnf', 'ws_dev', 'status',  'itens')
        #fields = '__all__'
 



    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        idnf = NotasFiscais.objects.create(**validated_data)
        for tr in itens_data:
            Itens.objects.create(idnf=idnf, **tr)
        return idnf

    def update(self, instance, validated_data):
        itens_data = validated_data.pop('itens')
  
        its = (instance.itens).all()
        its = list(its)
        instance.xNome_emit = validated_data.get('xNome_emit', instance.xNome_emit)
        instance.vBC = validated_data.get('vBC', instance.vBC)
        instance.vICMS = validated_data.get('vICMS', instance.vICMS)
        instance.vProd = validated_data.get('vProd', instance.vProd)
        instance.vFrete = validated_data.get('vFrete', instance.vFrete)
        instance.vSeg = validated_data.get('vSeg', instance.vSeg)
        instance.vDesc = validated_data.get('vDesc', instance.vDesc)
        instance.vII = validated_data.get('vII', instance.vII)
        instance.vIPI = validated_data.get('vIPI', instance.vIPI)
        instance.vIPIDevol = validated_data.get('vIPIDevol', instance.vIPIDevol)
        instance.vPIS = validated_data.get('vPIS', instance.vPIS)
        instance.vCOFINS = validated_data.get('vCOFINS', instance.vCOFINS)
        instance.vOutro = validated_data.get('vOutro', instance.vOutro)
        instance.vNF = validated_data.get('vNF', instance.vNF)
        instance.CNPJ_dest = validated_data.get('CNPJ_dest', instance.CNPJ_dest)
        instance.xNome_dest = validated_data.get('xNome_dest', instance.xNome_dest)
        instance.chNFe = validated_data.get('chNFe', instance.chNFe)
        #instance.dhRecbto = validated_data.get('dhRecbto', instance.dhRecbto)
        instance.xNome_dest = validated_data.get('xNome_dest', instance.xNome_dest)
        instance.save()
 
 
        for itens_data in itens_data:
            ite = its.pop(0)
            #ite.nItem = itens_data.get('nItem',ite.nItem)
            ite.cProd = itens_data.get('cProd',ite.cProd)
            #ite.nSku = itens_data.get('nSku',ite.nSku)
            ite.cEAN = itens_data.get('cEAN',ite.cEAN)
            ite.xProd = itens_data.get('xProd',ite.xProd)
            ite.NCM = itens_data.get('NCM',ite.NCM)
            ite.CFOP = itens_data.get('CFOP',ite.CFOP)
            ite.uCom = itens_data.get('uCom',ite.uCom)
            ite.qCom = itens_data.get('qCom',ite.qCom)
            ite.vUnCom = itens_data.get('vUnCom',ite.vUnCom)
            ite.vProd = itens_data.get('vProd',ite.vProd)
            ite.uTrib = itens_data.get('uTrib',ite.uTrib)
            ite.qTrib = itens_data.get('qTrib',ite.qTrib)
            ite.vUnTrib = itens_data.get('vUnTrib',ite.vUnTrib)
            #ite.vOutro = itens_data.get('vOutro',ite.vOutro)
            #ite.xPed = itens_data.get('xPed',ite.xPed)
            #ite.nItemPed = itens_data.get('nItemPed',ite.nItemPed)
            ite.save()
        return instance


class SkuSerializer(serializers.ModelSerializer):
  
      class Meta:
        model = Sku
        fields = '__all__'     


