from pedidos.models import Pedidos, Itens
from separacao.models import ItensSeparacao, Separacao
from rest_framework import serializers, fields
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ObjectDoesNotExist


class ItensSeparacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItensSeparacao
        fields = ('NUMSEQ', 'CODPROD', 'QTPROD', 'QTCONF', 'LOTFAB', 'DTFAB', 'DTVEN', 'status')



class SeparacaoSerializer(serializers.ModelSerializer):
    ITENS = ItensSeparacaoSerializer(many=True)

    class Meta:
        model = Separacao
        fields = ('NUMPEDCLI', 'CGCCLIWMS', 'CGCEMINF', 'QTVOL', 'CGCTRANSP', 'DTFIMCHECK', 'URLRAST','ITENS')



    def create(self, validated_data):
        numPedCli_data = validated_data.pop('ITENS')
        nNumPedCli = Separacao.objects.create(**validated_data)
        for item_data in numPedCli_data:
            ItensSeparacao.objects.create(nItens=nNumPedCli, **item_data)
        return nNumPedCli



    def update(self, instance, validated_data):
        numPedCli_data = validated_data.pop('ITENS')
        its = (instance.ITENS).all()
        its = list(its)
        instance.numeroPdd = validated_data.get('numeroPdd', instance.numeroNF)
        instance.save()
 
        for item_data in numPedCli_data:
            ite = its.pop(0)
            ite.numseq = item_data.get('NUMSEQ',ite.numseq)
            ite.codprod = item_data.get('CODPROD',ite.codprod)
            #ite.nSku = item_data.get('nSku',ite.nSku)
            ite.qtprod = item_data.get('QTPROD',ite.qtprod)
            ite.qtconf = item_data.get('QTCONF',ite.qtconf)
            ite.lotfab = item_data.get('LOTFAB',ite.lotfab)
            ite.dtfab = item_data.get('DTFAB',ite.dtfab)
            ite.dtven = item_data.get('DTVEN',ite.dtven)
            ite.save()
        return instance

    def validate(self, data):

        dd = Pedidos.objects.all()

        print(data)

        try:
            dados = Pedidos.objects.get(numpedcli = data['NUMPEDCLI'])
            
            # Pegar o id (pk) para fazer busca no Itens
            pdd_id = Pedidos.objects.filter(numpedcli = data['NUMPEDCLI']).values_list('pk', flat=True)
            # Pegar o registro em Itens através do idped_id (chave estrangeira)
            item_full = Itens.objects.filter(idped_id=pdd_id[0])
            #item abaixo que consta os dados enviados na nf para o WS
            vitemcod_item = item_full.values()

        except ObjectDoesNotExist:
            raise serializers.ValidationError({"mensagem erro": "Pedido/Cliente não encontrado: CNPJ Cliente:" + str(data['CGCCLIWMS']) + " - No. Pedido:" + data['NUMPEDCLI']})

        if len(data['ITENS']) == 0 :
            raise serializers.ValidationError({"mensagem erro": "077 -Nenhuma Mercadoria informada"})

        if 'QTVOL' not in data:
            raise serializers.ValidationError({"mensagem erro": "Qt. Volumes não informada - No. Pedido:" + data['NUMPEDCLI'] })

        if data['QTVOL'] == "" or data['QTVOL'] == "0":
            raise serializers.ValidationError({"messagem erro": "Qt. Volumes não informada - No. Pedido:" + data['NUMPEDCLI'] })

        else:
            ws_numseq_ok = ()
            nf_item = set()    

            ws_all_numseq = ()
            ws_all = set()



            ws_NUMSEQ = ()
            ws_acumulado_NUMSEQ = set()

            vitem_numseq = ()
            vitem_acumulado_numseq = set()

            for n in vitemcod_item:

                vitem_numseq = (int(n['numseq']))

                vitem_acumulado_numseq.add(vitem_numseq)


                v = 0
                for w in data['ITENS']:

                    ws_NUMSEQ =  (w['NUMSEQ'])

                    ws_acumulado_NUMSEQ.add(ws_NUMSEQ)
                    
                    if w['NUMSEQ'] == int(n['numseq']):

                        if str(n['codprod']) == w['CODPROD']:
                        
                        
                            if w['QTPROD'] == str(n['qtprod']):

                                if w['QTPROD'] == '1':
                                    data['ITENS'][v]['status'] = 1
                                else:
                                    data['ITENS'][v]['status'] = 2

                            else:

                                raise serializers.ValidationError({"mensagem erro": "Quantidade do Ítem Doc. Entrada divergente. NUMSEQ:" + str(w['NUMSEQ']) + " - No. Pedido:" + data['NUMPEDCLI'] })

                        else:
                            raise serializers.ValidationError({"mensagem erro": "CODPROD diverge do Cód. Merc. do Ítem Doc. Saída. NUMSEQ: :" + str(w['NUMSEQ']) + " Cód.Merc.: " + n['codprod']  + "-Cód. Merc.:" + w['CODPROD']})
           
                v = v + 1

            resultado = vitem_acumulado_numseq - ws_acumulado_NUMSEQ
            
            if len(resultado) > 0:

                raise serializers.ValidationError({"mensagem erro": "Checkout WMS/ERP incompleto. NUMSEQ:" + str(resultado)})


            try:
                nf = Pedidos.objects.get(numpedcli = data['NUMPEDCLI'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError({"mensagem erro": "Chave NF-e Recebida não encontrada"})

    
        return data
                
        


