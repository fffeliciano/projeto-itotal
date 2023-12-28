
from django.db import models
from datetime import datetime


class Pedidos(models.Model):
    CRIADO = 1
    LOGISTICA = 2
    ENVIADO = 3
    PENDENTE = 4
    CANCELADO = 5
    ENVIAR = 6
    IMPRESSO = 7
    REJEITADO = 8
    RETITENS_TYPES = (
        (CRIADO, 'Criado'),
        (LOGISTICA, 'Logistica'),
        (ENVIADO, 'Enviado'),
        (PENDENTE, 'Pendente'),
        (CANCELADO, 'Cancelado'),
        (ENVIAR, 'Enviar'),
        (IMPRESSO, 'Impresso'),
        (REJEITADO, 'Rejeitado')
    )

    numpedcli = models.CharField(max_length=50, primary_key=True)

    cgccliwms = models.PositiveBigIntegerField(default=38317322000131)
    cgceminf = models.PositiveBigIntegerField(default=38317322000131)
    obsped = models.CharField(max_length=200, blank=True)
    obsrom = models.CharField(max_length=200, blank=True)
    #numpedcli = models.CharField(max_length=50, unique=True)
    numpedrca = models.CharField(max_length=50,  blank=True, null=True)
    vltotped = models.DecimalField(max_digits=11, decimal_places=2)
    ect_tpserv = models.CharField(max_length=20, blank=True, null=True, default="")
    cgcdest = models.CharField(max_length=14)
    iedest =  models.CharField(max_length=20, blank=True, null=True, default="")
    nomedest = models.CharField(max_length=100)
    cepdest = models.CharField(max_length=8)
    ufdest = models.CharField(max_length=2)
    ibgemundest = models.CharField(max_length=7, blank=True)
    mun_dest = models.CharField(max_length=100)
    bair_dest = models.CharField(max_length=100)
    logr_dest = models.CharField(max_length=100)
    num_dest = models.CharField(max_length=6)
    comp_dest = models.CharField(max_length=50, blank=True)
    tp_frete = models.CharField(max_length=1, default='F')
    codvendedor = models.CharField(max_length=20, blank=True)
    nomevendedor = models.CharField(max_length=100, blank=True)
    dtinclusaoerp = models.DateField()
    dtliberacaoerp = models.DateField()
    dtEmbarque = models.DateTimeField(blank=True, null=True,)
    dtprev_ent_site = models.DateField(blank=True)
    integracao = models.CharField(max_length=50, blank=True, null=True)
    loja = models.CharField(max_length=40, blank=True, null=True)

    situacao = models.CharField(max_length=20, blank=True)
    
    numnf = models.PositiveIntegerField(null=True)
    serienf = models.CharField(max_length=3, blank=True, null=True)
    dteminf = models.DateTimeField(blank=True, null=True)
    vltotalnf = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    qtvol = models.PositiveIntegerField(null=True)
    chavenf = models.CharField(max_length=50, blank=True, null=True)
    
    danfefilename = models.CharField(max_length=200, blank=True, null=True)
    danfefilesize = models.IntegerField(blank=True, null=True)
    danfepdfbase64 = models.BinaryField(blank=True, null=True)

    emailrastro = models.CharField(max_length=200, blank=True, null=True, default="")
    dddrastro = models.CharField(max_length=2, blank=True, null=True)
    telrastro = models.CharField(max_length=50, blank=True, null=True , default=" - ") 
    cgc_transp = models.CharField(max_length=14)
    dtfimcheck = models.DateField(blank=True, null=True)
    urlrast = models.CharField(max_length=200, blank=True, null=True)
    uf_trp = models.CharField(max_length=2, blank=True, null=True)
    codigo_rastreamento = models.CharField(max_length=30, blank=True, null=True)
    
    #status = models.CharField(max_length=20, default="novo")
    tamanhoEtiqueta = models.CharField(max_length=10, blank=True, null=True)
    labelVerified = models.BooleanField(default=False)
    #etiquetaZPLBase64 = models.TextField(null=True)



    cdblq_clg = models.CharField(max_length=30, blank=True, null=True, default="")
    prioridade = models.CharField(max_length=30, blank=True, null=True)
    cod_carga = models.CharField(max_length=150, blank=True, null=True, default="")

    rejeicao = models.CharField(max_length=250, blank=True, null=True, default="")
    status = models.PositiveSmallIntegerField(choices=RETITENS_TYPES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
       
    def __str__(self):
        return self.numpedcli

    class Meta:
        ordering = ('-updated_at',)


class Itens(models.Model):
    
    idped = models.ForeignKey(Pedidos,related_name='itens', on_delete=models.CASCADE)
     
    #numseq = models.IntegerField(primary_key=True, blank=True)
    #numseq_old = models.IntegerField(blank=True, null=True)
    numseq = models.CharField(max_length=5)
    codprod = models.CharField(max_length=20)
    qtprod = models.IntegerField()

    qtconf = models.IntegerField(blank=True, null=True)
    lotfab = models.CharField(max_length=100, blank=True, null=True)
    dtfab = models.DateField(blank=True, null=True)
    dtven = models.DateField(blank=True, null=True)
    #nser = models.CharField(max_length=100)
    vlr_unit = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    cdblq_prod = models.CharField(max_length=30, blank=True, null=True, default="")

    
    


    def __str__(self):
        return self.codprod
    




'''
class EmbarqueOLD(models.Model):

    #NUMPEDCLI = models.ForeignKey(Pedidos,related_name='numpedcli_new', on_delete=models.CASCADE, unique=True)


    #NUMPEDCLI = models.ForeignKey(Pedidos,related_name='numpedcli_new', on_delete=models.CASCADE)

    NUMPEDCLI = models.OneToOneField(Pedidos, on_delete=models.CASCADE, primary_key=True)

    CGCCLIWMS = models.PositiveBigIntegerField(default=38317322000131)
    TIPO_EVENTO = models.CharField(max_length=1)
    DT_HR_EVENTO = models.DateTimeField()
    #DT_HR_EVENTO = models.DateTimeField()
    #, input_formats=["%Y-%m-%dT%H:%M", ]


    CGCTRANSP = models.CharField(max_length=14)
    NUM_DOC_EMB = models.IntegerField()
    QT_PED_EMB = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
       
    def __str__(self):
        return str(self.NUMPEDCLI)

    class Meta:
        ordering = ('-updated_at',)

'''


#--- copia Embarque -----------------------------------------------------------------------------inicio--

class Embarque(models.Model):
    # Para não ter incompatibilidade , tiver que criar primeiro o campo NUMPEDCLI como campo normal e depois alteri usaando o WORKBENCH e marquei com o cursor o campo NUMPEDCLI e em baixo alterei Charset/Collation: para UTF8, assim ele passou sem gerar erros de incompatilidade dando o erro abaixo :
    # ERROR 3780: Referencing column 'numpedcli' and referenced column 'numpedcli' in foreign key constraint 'numpedcli' are incompatible.

    NUMPEDCLI = models.ForeignKey(Pedidos,related_name='numpedcliOne', on_delete=models.CASCADE)

    CGCCLIWMS = models.PositiveBigIntegerField(default=38317322000131)
    TIPO_EVENTO = models.CharField(max_length=1)
    DT_HR_EVENTO = models.DateTimeField()
    CGCTRANSP = models.CharField(max_length=14)
    NUM_DOC_EMB = models.IntegerField()
    QT_PED_EMB = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
       
    def __str__(self):
        return str(self.NUMPEDCLI)

    class Meta:
        ordering = ('-updated_at',)


#-------------------------------------------------------------------------------------------------
# Notas Fiscais
#-------------------------------------------------------------------------------------------------
# Início

class NotasFiscaisSaida(models.Model):
    CRIADO = 1
    LOGISTICA = 2
    ENVIADO = 3
    PENDENTE = 4
    CANCELADO = 5
    ENVIAR = 6
    IMPRESSO = 7
    REJEITADO = 8
    RETITENS_TYPES = (
        (CRIADO, 'Criado'),
        (LOGISTICA, 'Logistica'),
        (ENVIADO, 'Enviado'),
        (PENDENTE, 'Pendente'),
        (CANCELADO, 'Cancelado'),
        (ENVIAR, 'Enviar'),
        (IMPRESSO, 'Impresso'),
        (REJEITADO, 'Rejeitado')
    )

    codNfSerie = models.CharField(max_length=20, primary_key=True)

    numpedcli = models.CharField(max_length=50, blank=True, null=True)

    cgccliwms = models.PositiveBigIntegerField(default=38317322000131)
    cgceminf = models.PositiveBigIntegerField(default=38317322000131)
    
        
    numnf = models.PositiveIntegerField()
    serienf = models.CharField(max_length=3)
    dteminf = models.DateTimeField()
    vltotalnf = models.DecimalField(max_digits=11, decimal_places=2)
    qtvol = models.PositiveIntegerField()
    chavenf = models.CharField(max_length=50)

    xmlNf = models.CharField(max_length=160, blank=True, null=True)
    linkDanfe = models.CharField(max_length=100, blank=True, null=True)
    situacao = models.CharField(max_length=30, blank=True,  null=True)


    
    danfefilename = models.CharField(max_length=60, blank=True, null=True)
    danfefilesize = models.CharField(max_length=60, blank=True, null=True)
    danfepdfbase64 = models.BinaryField(blank=True, null=True)

    cgc_transp = models.CharField(max_length=20, blank=True, null=True)
    
    #status = models.CharField(max_length=20, default="novo")
    rejeicao = models.CharField(max_length=250, blank=True, null=True, default="")
    status = models.PositiveSmallIntegerField(choices=RETITENS_TYPES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    lixo = models.DateTimeField(auto_now=True, editable=False)
       
    def __str__(self):
        return self.numpedcli

    class Meta:
        ordering = ('-numnf',)


class  ItensNF(models.Model):
    
    idped = models.ForeignKey(NotasFiscaisSaida,related_name='itens', on_delete=models.CASCADE)
     
    #numseq = models.IntegerField(primary_key=True, blank=True)
    #numseq_old = models.IntegerField(blank=True, null=True)
    numseq = models.CharField(max_length=5)
    codprod = models.CharField(max_length=20)
    qtprod = models.IntegerField()

    #nser = models.CharField(max_length=100)
    vlr_unit = models.DecimalField(max_digits=12, decimal_places=2, null=True) 


    def __str__(self):
        return self.codprod


#-------------------------------------------------------------------------------------------------


#--- copia Embarque -----------------------------------------------------------------------------inicio--
"""
class Etiquetas(models.Model):
    # Para não ter incompatibilidade , tiver que criar primeiro o campo NUMPEDCLI como campo normal e depois alteri usaando o WORKBENCH e marquei com o cursor o campo NUMPEDCLI e em baixo alterei Charset/Collation: para UTF8, assim ele passou sem gerar erros de incompatilidade dando o erro abaixo :
    # ERROR 3780: Referencing column 'numpedcli' and referenced column 'numpedcli' in foreign key constraint 'numpedcli' are incompatible.

    numpedcli = models.ForeignKey(Pedidos,related_name='numpedclietq', on_delete=models.CASCADE)

    danfepdfbase64 = models.BinaryField(blank=True, null=True)
    tamanhoEtiqueta = models.CharField(max_length=10, blank=True, null=True)
    etiquetaZPLBase64 = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
       
    def __str__(self):
        return str(self.numpedcli)

    class Meta:
        ordering = ('-updated_at',)

"""
#-------------------------------------------------------------------------------------------------
