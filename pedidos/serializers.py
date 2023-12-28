from pedidos.models import Pedidos, Itens, Embarque, NotasFiscaisSaida,  ItensNF
#from pedidos.models import Pedidos, Itens, NotasFiscaisSaida,  ItensNF, EmbarqueFour


from rest_framework import serializers


class ItensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itens
        fields = ('numseq', 'codprod', 'qtprod', 'vlr_unit', 'cdblq_prod')
        #fields = ('numseq', 'codprod', 'qtprod', 'qtconf', 'lotfab', 'dtfab', 'dtven', 'vlr_unit')
 


class PedidosSerializer(serializers.ModelSerializer):
    itens = ItensSerializer(many=True)

    class Meta:
        model = Pedidos
        fields = ('cgccliwms', 'cgceminf', 'obsped', 'obsrom', 'numpedcli', 'numpedrca', 'vltotped','ect_tpserv' ,'cgcdest', 'iedest','nomedest', 'cepdest', 'ufdest', 'ibgemundest', 'mun_dest', 'bair_dest', 'logr_dest', 'num_dest', 'comp_dest', 'tp_frete', 'codvendedor', 'nomevendedor', 'dtinclusaoerp', 'dtliberacaoerp', 'dtEmbarque', 'dtprev_ent_site', 'integracao', 'loja', 'emailrastro', 'dddrastro', 'telrastro', 'numnf', 'serienf', 'dteminf', 'vltotalnf', 'qtvol', 'chavenf', 'cgc_transp', 'uf_trp', 'labelVerified' , 'status', 'rejeicao' ,'codigo_rastreamento', 'tamanhoEtiqueta', 'cdblq_clg', 'prioridade', 'cod_carga', 'itens')
        #fields = ('numpedcli', 'cgccliwms', 'cgceminf', 'obsped', 'obsrom','numpedrca', 'vltotped', 'cgcdest', 'nomedest', 'cepdest', 'ufdest', 'ibgemundest', 'mun_dest', 'bair_dest', 'logr_dest', 'num_dest', 'comp_dest', 'tp_frete', 'codvendedor', 'nomevendedor', 'dtinclusaoerp', 'dtliberacaoerp', 'dtprev_ent_site', 'numnf', 'serienf', 'dteminf', 'vltotalnf', 'qtvol', 'chavenf', 'danfefilename', 'danfefilesize', 'danfepdfbase64', 'emailrastro', 'dddrastro', 'telrastro', 'cgc_transp', 'dtfimcheck', 'urlrast', 'uf_trp', 'itens')
        #fields = ('numpedcli', 'cgccliwms', 'cgceminf', 'obsped', 'obsrom','numpedrca', 'vltotped', 'cgcdest', 'nomedest', 'cepdest', 'ufdest', 'ibgemundest', 'mun_dest', 'bair_dest', 'logr_dest', 'num_dest', 'comp_dest', 'tp_frete', 'codvendedor', 'nomevendedor', 'dtinclusaoerp', 'dtliberacaoerp', 'dtprev_ent_site', 'numnf', 'serienf', 'dteminf', 'vltotalnf', 'qtvol', 'chavenf', 'danfefilename', 'danfefilesize', 'danfepdfbase64', 'emailrastro', 'dddrastro', 'telrastro', 'cgc_transp', 'dtfimcheck', 'urlrast', 'uf_trp', 'itens')
        

    
#-----------------------------------------------------------


    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        var = Pedidos.objects.create(**validated_data)
        for tr in itens_data:
            Itens.objects.create(idped=var, **tr)
        return var

    def update(self, instance, validated_data):
        itens_data = validated_data.pop('itens')
        its = (instance.itens).all()
        its = list(its)
        instance.cgceminf = validated_data.get('cgceminf', instance.cgceminf)
        instance.cgccliwms = validated_data.get('cgccliwms', instance.cgccliwms)
        instance.numpedcli = validated_data.get('numpedcli', instance.numpedcli)
        instance.qtvol = validated_data.get('qtvol', instance.qtvol)
        instance.cgc_transp = validated_data.get('cgc_transp', instance.cgc_transp)
        instance.codigo_rastreamento = validated_data.get('codigo_rastreamento', instance.codigo_rastreamento)
        instance.tamanhoEtiqueta = validated_data.get('tamanhoEtiqueta', instance.tamanhoEtiqueta)
        instance.labelVerified = validated_data.get('labelVerified', instance.labelVerified)
        instance.rejeicao = validated_data.get('rejeicao', instance.rejeicao)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        for item_data in itens_data:
            ite = its.pop(0)
            ite.numseq = item_data.get('numseq',ite.numseq)
            ite.codprod = item_data.get('codprod', ite.codprod)
            ite.qtprod = item_data.get('qtprod', ite.qtprod)
            ite.qtconf = item_data.get('qtconf', ite.qtconf)
            ite.lotfab = item_data.get('lotfab', ite.lotfab)
            ite.dtfab = item_data.get('dtfab', ite.dtfab)
            ite.dtven = item_data.get('dtven', ite.dtven)
            ite.save()
        return instance

   

# Notas Fiscais
#-------------------------------------------------------------------------------------

class ItensNFSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ItensNF
        fields = ('numseq', 'codprod', 'qtprod', 'vlr_unit')
        #fields = ('numseq', 'codprod', 'qtprod', 'qtconf', 'lotfab', 'dtfab', 'dtven', 'vlr_unit')
 


class NotasFiscaisSaidaSerializer(serializers.ModelSerializer):
    itens = ItensNFSerializer(many=True)

    class Meta:
        model = NotasFiscaisSaida
        fields = ('cgccliwms', 'cgceminf', 'codNfSerie', 'numpedcli', 'numnf', 'serienf', 'dteminf', 'vltotalnf', 'qtvol', 'chavenf', 'situacao', 'danfefilename', 'danfefilesize', 'xmlNf', 'linkDanfe','cgc_transp', 'rejeicao', 'status', 'itens')
        #fields = ('numpedcli', 'cgccliwms', 'cgceminf', 'obsped', 'obsrom','numpedrca', 'vltotped', 'cgcdest', 'nomedest', 'cepdest', 'ufdest', 'ibgemundest', 'mun_dest', 'bair_dest', 'logr_dest', 'num_dest', 'comp_dest', 'tp_frete', 'codvendedor', 'nomevendedor', 'dtinclusaoerp', 'dtliberacaoerp', 'dtprev_ent_site', 'numnf', 'serienf', 'dteminf', 'vltotalnf', 'qtvol', 'chavenf', 'danfefilename', 'danfefilesize', 'danfepdfbase64', 'emailrastro', 'dddrastro', 'telrastro', 'cgc_transp', 'dtfimcheck', 'urlrast', 'uf_trp', 'itens')
        #fields = ('numpedcli', 'cgccliwms', 'cgceminf', 'obsped', 'obsrom','numpedrca', 'vltotped', 'cgcdest', 'nomedest', 'cepdest', 'ufdest', 'ibgemundest', 'mun_dest', 'bair_dest', 'logr_dest', 'num_dest', 'comp_dest', 'tp_frete', 'codvendedor', 'nomevendedor', 'dtinclusaoerp', 'dtliberacaoerp', 'dtprev_ent_site', 'numnf', 'serienf', 'dteminf', 'vltotalnf', 'qtvol', 'chavenf', 'danfefilename', 'danfefilesize', 'danfepdfbase64', 'emailrastro', 'dddrastro', 'telrastro', 'cgc_transp', 'dtfimcheck', 'urlrast', 'uf_trp', 'itens')
        

    
#-----------------------------------------------------------


    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        var = NotasFiscaisSaida.objects.create(**validated_data)
        for tr in itens_data:
             ItensNF.objects.create(idped=var, **tr)
        return var

    def update(self, instance, validated_data):
        itens_data = validated_data.pop('itens')
        its = (instance.itens).all()
        its = list(its)
        instance.situacao = validated_data.get('situacao', instance.situacao)
        instance.danfefilename = validated_data.get('danfefilename', instance.danfefilename)
        instance.danfefilesize = validated_data.get('danfefilesize', instance.danfefilesize)
        instance.xmlNf = validated_data.get('xmlNf', instance.xmlNf)
        instance.linkDanfe = validated_data.get('linkDanfe', instance.linkDanfe)
        instance.rejeicao = validated_data.get('rejeicao', instance.rejeicao)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        for item_data in itens_data:
            ite = its.pop(0)
            ite.numseq = item_data.get('numseq',ite.numseq)
            ite.codprod = item_data.get('codprod', ite.codprod)
            ite.qtprod = item_data.get('qtprod', ite.qtprod)
            ite.save()
        return instance






# Embarque
#-------------------------------------------------------------------------------------

class EmbarqueSerializer(serializers.ModelSerializer):
    
    DT_HR_EVENTO = serializers.DateTimeField(input_formats=["%d/%m/%y %H:%M:%S", ])
    #DT_HR_EVENTO = serializers.DateTimeFieldWihTZ(input_formats=["%d/%m/%Y %H:%M:%S", ])

    class Meta:
        model = Embarque
        fields = ('NUMPEDCLI', 'CGCCLIWMS', 'TIPO_EVENTO', 'DT_HR_EVENTO', 'CGCTRANSP', 'NUM_DOC_EMB', 'QT_PED_EMB' )



"""
# EmbarqueFour
#-------------------------------------------------------------------------------------

class EmbarqueFourSerializer(serializers.ModelSerializer):
    
    DT_HR_EVENTO = serializers.DateTimeField(input_formats=["%d/%m/%y %H:%M:%S", ])
    #DT_HR_EVENTO = serializers.DateTimeFieldWihTZ(input_formats=["%d/%m/%Y %H:%M:%S", ])

    class Meta:
        model = EmbarqueFour
        fields = ('NUMPEDCLI', 'CGCCLIWMS', 'TIPO_EVENTO', 'DT_HR_EVENTO', 'CGCTRANSP', 'NUM_DOC_EMB', 'QT_PED_EMB' )
        """



# Embarque
#-------------------------------------------------------------------------------------
"""
class EtiquetasSerializer(serializers.ModelSerializer):
    
    #DT_HR_EVENTO = serializers.DateTimeField(input_formats=["%d/%m/%y %H:%M:%S", ])
    #DT_HR_EVENTO = serializers.DateTimeFieldWihTZ(input_formats=["%d/%m/%Y %H:%M:%S", ])

    class Meta: 
        model = Etiquetas
        fields = ('numpedcli', 'danfepdfbase64', 'tamanhoEtiqueta', 'etiquetaZPLBase64')
"""




 
