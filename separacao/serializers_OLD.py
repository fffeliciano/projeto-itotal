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




    # ---  REFAZER A PARTE DE BAIXO :
    # 
    # 
    #  
    def validate(self, data):
        #print("NUMPEDCLI ===>", data['NUMPEDCLI'])
        print("data=========>", data)

    # Buscar no Rest Pedidos, o arquivo com dados da nf para conferência


        print("cheguei aqui!!!")    

        print(data['NUMPEDCLI'])
        print(type(data['NUMPEDCLI']))
        
        dd = Pedidos.objects.all()
        print(dd.values)

        #dd1 = Pedidos.objects.get(numpedcli = data['NUMPEDCLI'])
        #exit(95)

        try:
            dados = Pedidos.objects.get(numpedcli = data['NUMPEDCLI'])
            print(" dados do Pedido ===>>", dados)



            
            
            # Pegar o id (pk) para fazer busca no Itens
            pdd_id = Pedidos.objects.filter(numpedcli = data['NUMPEDCLI']).values_list('pk', flat=True)
            # Pegar o registro em Itens através do idped_id (chave estrangeira)
            item_full = Itens.objects.filter(idped_id=pdd_id[0])
            #item abaixo que consta os dados enviados na nf para o WS
            vitemcod_item = item_full.values()
            print("vitemcod_item----->", vitemcod_item )
            
        # ('NUMPEDCLI', '222496'), ('CGCCLIWMS', 38317322000131)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"mensagem erro": "Pedido/Cliente não encontrado: CNPJ Cliente:" + str(data['CGCCLIWMS']) + " - No. Pedido:" + data['NUMPEDCLI']})

        #print("nf---------->>", dados)
        print("---data-------->", data['ITENS'])
        print("---data-------->", data['QTVOL'])
        print("---type data-------->", type(data['QTVOL']))
        print("len--->", len(data['ITENS']))

        


 
        # WS
        if len(data['ITENS']) == 0 :
            raise serializers.ValidationError({"mensagem erro": "077 -Nenhuma Mercadoria informada"})


     
        # WS
        else:
            
        #    if n['QTPROD'] < 10 :
        #            print("Erro Qtde produto ====>" , n['QTPROD'])
        #            raise serializers.ValidationError({"qtde de produtos": "está menor que 10"})
        #tirar este trecho e colocar nova avaliação 
         
            print(" avaliação da qtvol ====>", data['QTVOL'])
            print(" avaliação type qtvol ====>", type(data['QTVOL']))


            if data['QTVOL']:
                pass
            else:
                raise serializers.ValidationError({"mensagem erro": "Qt. Volumes não informada - No. Pedido:" + data['NUMPEDCLI'] })
         
       
            ws_numseq_ok = ()
            ws_all_numseq = ()
            ws_all = set()
            nf_item = set()
            # WS
            for n in vitemcod_item:



            #w_vaNUMSEQ = set()
            v = 0
            for w in data['ITENS']:
                #print("--JSON RECEBIDO-----------------------------------------------------------") 
                ws_all_numseq = (w['NUMSEQ'])
                print(ws_all_numseq)
                print("Numero da rodada Principal w---->", w)
                print("id--data---->", w["NUMSEQ"])
                print("v==>", v)


                #w_vaNUMSEQ.add(w["NUMSEQ"])

                # NF

                #vaNumseq = set()
                for n in vitemcod_item:
                    print("---------------------------------------------------------Pedido ITENS---")    
                    print("n-RetItens-->", n)
                    print("id--RetItens--->", n['id'])
                    
                    print( "str(n['numseq'])=====>" , int(n['numseq']))
                    print(type(int(n['numseq'])))

                    print("w['NUMSEQ']===========>", w['NUMSEQ'])
                    print(type(w['NUMSEQ']))

                    #vaNumseq.add(int(n['numseq']))
                    #exit(97)
                    
                    if w['NUMSEQ'] == int(n['numseq']):

                        print( " W ===================== N" )

                        ws_numseq_ok = (w['NUMSEQ'])
                        print("ws_numseq_ok=====>", ws_numseq_ok)
                        
                        if str(n['codprod']) == w['CODPROD']:
                        
                        
                            if w['QTPROD'] == str(n['qtprod']):

                                if w['QTPROD'] == '1':
                                    data['ITENS'][v]['status'] = 1
                                else:
                                    data['ITENS'][v]['status'] = 2

                            else:
                                #if w['QTPROD']:
                                #    pass
                                #else:
                                #    raise serializers.ValidationError({"mensagem erro": "Qt. Volumes não informada - No. Pedido:" + data['NUMPEDCLI'] })
                                raise serializers.ValidationError({"mensagem erro": "Quantidade do Ítem Doc. Entrada divergente. NUMSEQ:" + str(w['NUMSEQ']) + " - No. Pedido:" + data['NUMPEDCLI'] })

                        else:
                            raise serializers.ValidationError({"mensagem erro": "CODPROD diverge do Cód. Merc. do Ítem Doc. Saída. NUMSEQ: :" + str(w['NUMSEQ']) + " Cód.Merc.: " + n['codprod']  + "-Cód. Merc.:" + w['CODPROD']})
                    nf_item.add(ws_numseq_ok)
                    print("nf_item===>", nf_item)

                ws_all.add(ws_all_numseq)
                print("origem ws_all",ws_all)
                
                print("ws_all - nf_item > 0 ", ws_all, nf_item)
                
                if (ws_all - nf_item):
                    print("++++++++++++++++++++++ tem algo aqui +++++++++++++++++++")
                else: 
                    print(" --------------------- não achei nada __________________")

                #exit(87)

                print("len ws_all-nf_item ---------------->", len(ws_all-nf_item))
                
                if len(ws_all-nf_item) > 0:
                    print("tamanho len ws_all - nf_item :", len(ws_all-nf_item))
                    raise serializers.ValidationError({"mensagem erro": "Ítem Doc. Entrada não encontrado.NUMSEQ:" + str(ws_all-nf_item)})
                
                v = v + 1

            try:
                nf = Pedidos.objects.get(numpedcli = data['NUMPEDCLI'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError({"mensagem erro": "Chave NF-e Recebida não encontrada"})

            #print("vaNumseq------->", vaNumseq)

            #print("w_vaNUNSEQ=====", w_vaNUMSEQ )

            #print("Diferença entre vaNumseq - W_vaNUMSEQ =",  vaNumseq-w_vaNUMSEQ )
            
            
            exit(99)

        
        #print("print data ----->>", data)
        #exit(8)    
        return data
                
        


