from fornecedor.models import NotasFiscais, Itens, Sku, RetornoItensNFEntrada, RetItens
from rest_framework import serializers, fields

from rest_framework.validators import UniqueTogetherValidator

from django.core.exceptions import ObjectDoesNotExist



class RetItensSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetItens
        fields = ('NUMSEQ', 'CODPROD', 'QTPROD', 'QTAVARIA', 'QTFALTA', 'NSER' , 'LOTFAB', 'DTFAB', 'DTVEN', 'numeroNF')

        
class RetornoItensNFEntradaSerializer(serializers.ModelSerializer):
    ITEMS = RetItensSerializer(many=True)

    class Meta:
        model = RetornoItensNFEntrada
        fields = ('CHAVENFE', 'ITEMS')

    def create(self, validated_data):
        chave_nf_data = validated_data.pop('ITEMS')
        nChaveNF = RetornoItensNFEntrada.objects.create(**validated_data)
        for item_data in chave_nf_data:
            RetItens.objects.create(numeroNF=nChaveNF, **item_data)
        return nChaveNF



    def update(self, instance, validated_data):
        chave_nf_data = validated_data.pop('ITEMS')
        its = (instance.ITEMS).all()
        its = list(its)
        instance.numeroNF = validated_data.get('numeroNF', instance.numeroNF)
        instance.save()
 
        for item_data in chave_nf_data:
            ite = its.pop(0)
            ite.numseq = item_data.get('numseq',ite.numseq)
            ite.codprod = item_data.get('codprod',ite.codprod)
            #ite.nSku = item_data.get('nSku',ite.nSku)
            ite.qtprod = item_data.get('qtprod',ite.qtprod)
            ite.qtavaria = item_data.get('qtavaria',ite.qtavaria)
            ite.qtfalta = item_data.get('qtfalta',ite.qtfalta)
            ite.nser = item_data.get('nser',ite.nser)
            ite.lotfab = item_data.get('lotfab',ite.lotfab)
            ite.dtfab = item_data.get('dtfab',ite.dtfab)
            ite.dtven = item_data.get('dtven',ite.dtven)
            ite.save()
        return instance

    
    def validate(self, data):
        #print("chaveNFE ===>", data['CHAVENFE'])
        #print(data)

    # Buscar no Rest NotasFiscais, o arquivo com dados da nf para conferência


        try:
            dados = NotasFiscais.objects.get(chNFe = data['CHAVENFE'])
            #print("nf===>>", dados)

            # Pegar o id (pk) para fazer busca no Itens
            nota_id = NotasFiscais.objects.filter(chNFe = data['CHAVENFE']).values_list('pk', flat=True)
            # Pegar o registro em Itens através do idnf_id (chave estrangeira)
            item_full = Itens.objects.filter(idnf_id=nota_id[0])
            #item abaixo que consta os dados enviados na nf para o WS
            vitemcod_item = item_full.values()
            #print("vitemcod_item----->", vitemcod_item )
            

        except ObjectDoesNotExist:
            raise serializers.ValidationError({"mensagem erro": "Chave NF-e Recebida não encontrada"})

        #print("nf---------->>", dados)
        #print("---data-------->", data['ITEMS'])
        #print("len--->", len(data['ITEMS']))

 
        # WS
        if len(data['ITEMS']) == 0 :
            raise serializers.ValidationError({"mensagem erro": "077 -Nenhuma Mercadoria informada"})
     
        # WS
        else:
            
        #    if n['QTPROD'] < 10 :
        #            print("Erro Qtde produto ====>" , n['QTPROD'])
        #            raise serializers.ValidationError({"qtde de produtos": "está menor que 10"})
        #tirar este trecho e colocar nova avaliação    
            ws_numseq_ok = ()
            ws_all_numseq = ()
            ws_all = set()
            nf_item = set()
            # WS

            v = 0
            for w in data['ITEMS']:
                #print("--JSON RECEBIDO-----------------------------------------------------------") 
                ws_all_numseq = (w['NUMSEQ'])
                print(ws_all_numseq)
                #print("Numero da rodada Principal w---->", w)
                #print("id--data-->", w["NUMSEQ"])
                #print("v==>", v)

                # NF
                for n in vitemcod_item:
                    #print("---------------------------------------------------------NOTA FISCAL ITENS---")    
                    #print("n-RetItens-->", n)
                    #print("id--RetItens--->", n['id'])

                    if w['NUMSEQ'] == n['nItem']:
                        ws_numseq_ok = (w['NUMSEQ'])
                        
                        if str(n['nsku']) == w['CODPROD']:
                        
                            data['status'] = 3
                            #if w['QTPROD'] == n['qCom']:
                                
                            #    data['ITEMS'][v]['status'] = 2
                            #else:
                            #    
                            #    data['ITEMS'][v]['status'] = 3

                        else:
                            raise serializers.ValidationError({"mensagem erro": "CODPROD diverge do Cód. Merc. do Ítem Doc. Entrada. CODPROD:" + w['CODPROD'] + " Cód.Merc.: " + str(n['nsku'])  + "- Chave NF-e:" })
                    nf_item.add(ws_numseq_ok)
                    print("nf_item===>", nf_item)

                ws_all.add(ws_all_numseq)
                print("origem ws_all",ws_all)
                
                print("ws_all-nf_item > 0 ", ws_all, nf_item)

                print("len ws_all-nf_item ---------------->", len(ws_all-nf_item))
                
                if len(ws_all-nf_item) > 0:
                    print("tamanho len ws_all - nf_item :", len(ws_all-nf_item))
                    raise serializers.ValidationError({"mensagem erro": "Ítem Doc. Entrada não encontrado.NUMSEQ:" + str(ws_all-nf_item)})
                
                v = v + 1

            try:
                nf = NotasFiscais.objects.get(chNFe = data['CHAVENFE'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError({"mensagem erro": "Chave NF-e Recebida não encontrada"})


        
        #print("print data ----->>", data)
        #exit(8)    
        return data
                
        



#-----------------------------------------------------------------------fim
class ItensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itens
        fields = ( 'nItem', 'cProd', 'cEAN', 'xProd', 'NCM', 'CFOP', 'uCom', 'qCom', 'vUnCom', 'vProd', 'cEANTrib','uTrib', 'qTrib', 'vUnTrib', 'indTot', 'ean' ,'nsku')
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
        for item_data in itens_data:
            Itens.objects.create(idnf=idnf, **item_data)
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
 
 
        for item_data in itens_data:
            ite = its.pop(0)
            #ite.nItem = item_data.get('nItem',ite.nItem)
            ite.cProd = item_data.get('cProd',ite.cProd)
            #ite.nSku = item_data.get('nSku',ite.nSku)
            ite.cEAN = item_data.get('cEAN',ite.cEAN)
            ite.xProd = item_data.get('xProd',ite.xProd)
            ite.NCM = item_data.get('NCM',ite.NCM)
            ite.CFOP = item_data.get('CFOP',ite.CFOP)
            ite.uCom = item_data.get('uCom',ite.uCom)
            ite.qCom = item_data.get('qCom',ite.qCom)
            ite.vUnCom = item_data.get('vUnCom',ite.vUnCom)
            ite.vProd = item_data.get('vProd',ite.vProd)
            ite.uTrib = item_data.get('uTrib',ite.uTrib)
            ite.qTrib = item_data.get('qTrib',ite.qTrib)
            ite.vUnTrib = item_data.get('vUnTrib',ite.vUnTrib)
            #ite.vOutro = item_data.get('vOutro',ite.vOutro)
            #ite.xPed = item_data.get('xPed',ite.xPed)
            #ite.nItemPed = item_data.get('nItemPed',ite.nItemPed)
            ite.save()
        return instance


class SkuSerializer(serializers.ModelSerializer):
  
      class Meta:
        model = Sku
        fields = ('sku', 'ean', 'nomeProduto')
        #fields = '__all__'    



