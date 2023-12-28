from django.db import models

from datetime import datetime, timezone

class Sku(models.Model):
    sku = models.AutoField(primary_key=True) 
    ean = models.CharField(max_length=13, unique=True)
    nomeProduto = models.CharField(max_length=150) 
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    
    def __str__(self):
        return self.nomeProduto

    class  Meta:
        ordering = ('-updated_at',)


class NotasFiscais(models.Model):

    PENDENTE = 1
    ENVIADO = 2
    RETITENS_TYPES = (
        (PENDENTE, 'Pendente'),
        (ENVIADO, 'Enviado'),
    )


   
    chNFe = models.CharField(max_length=50, unique=True)       #": "26201124073694000155550010005769651017370034",
 
    natOp = models.CharField(max_length=70)       #": "VENDA MERCADORIAS ADQUIRIDAS E/OU RECEB TERCEIROS",
    
    serie = models.CharField(max_length=2)     #": "1",
    nNF = models.CharField(max_length=12)        #": "576965",
    dhEmi = models.DateTimeField()     #": "2020-11-04T17:26:54-03:00",

    CNPJ_emit = models.CharField(max_length=14)       #": "24073694000155",
    xNome_emit = models.CharField(max_length=60)     #": "CIL   COMERCIO DE INFORMATICA LTDA",

    vBC = models.DecimalField(max_digits=12, decimal_places=2)        #": "10791.50",
    vICMS = models.DecimalField(max_digits=12, decimal_places=2)       #": "431.66",
    vProd = models.DecimalField(max_digits=12, decimal_places=2)       #": "10790.00",
    vFrete = models.DecimalField(max_digits=12, decimal_places=2)      #": "0.00",
    vSeg = models.DecimalField(max_digits=12, decimal_places=2)        #": "0.00",
    vDesc = models.DecimalField(max_digits=12, decimal_places=2)       #": "0.00",
    vII = models.DecimalField(max_digits=12, decimal_places=2)         #": "0.00",
    vIPI = models.DecimalField(max_digits=12, decimal_places=2)        #": "0.00",
    vIPIDevol = models.DecimalField(max_digits=12, decimal_places=2)   #": "0.00",
    vPIS = models.DecimalField(max_digits=12, decimal_places=2)        #": "170.94",
    vCOFINS = models.DecimalField(max_digits=12, decimal_places=2)      #": "787.35",
    vOutro = models.DecimalField(max_digits=12, decimal_places=2)      #": "1.50",
    vNF = models.DecimalField(max_digits=12, decimal_places=2)         #": "10791.50"

    CNPJ_dest = models.CharField(max_length=14, blank=True)        #": "05560270000170",
    xNome_dest = models.CharField(max_length=60)       #": "IDCOM COMERCIO EIRELI ME",

    #ws_tpdestnf = models.CharField(max_length=1, default='2')
    ws_tpdestnf = models.CharField(max_length=1)
    #ws_dev = models.CharField(max_length=1, default='0')
    ws_dev = models.CharField(max_length=1)
    
    status = models.PositiveSmallIntegerField(choices=RETITENS_TYPES, blank=True, null=True)
    #status_old  = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self):
        return self.nNF

    class Meta:
        ordering =  ('-updated_at',)


class Itens(models.Model):
 
    idnf = models.ForeignKey(NotasFiscais, related_name='itens',on_delete=models.CASCADE)

    nItem = models.IntegerField()
    cProd  = models.CharField(max_length=20)  #": "490750",
    cEAN = models.CharField(max_length=13)         #": "6925281928062",
    xProd = models.CharField(max_length=150)        #": "Fone de Ouvido JBL T110BT Bluetooth Branco",
    NCM = models.CharField(max_length=10)          #": "85183000",
    CFOP = models.CharField(max_length=10)         #": "6102",
    uCom = models.CharField(max_length=5)         #": "UN",
    qCom = models.DecimalField(max_digits=12, decimal_places=2)        #": "100.0000",
    vUnCom = models.DecimalField(max_digits=12, decimal_places=2)      #": "107.90000",
    vProd = models.DecimalField(max_digits=12, decimal_places=2)      #": "10790.00",
    cEANTrib =  models.CharField(max_length=13)
    uTrib = models.CharField(max_length=5)        #": "UN",
    qTrib = models.DecimalField(max_digits=12, decimal_places=2)      #": "100.0000",
    vUnTrib = models.DecimalField(max_digits=12, decimal_places=2)     #": "107.90000",
   
    indTot = models.CharField(max_length=10)     #": "1",
    nsku = models.IntegerField()



    ean = models.ForeignKey(Sku, to_field="ean", db_column="ean" ,on_delete=models.CASCADE)

    def __str__(self):
        return self.xProd


class RetornoItensNFEntrada(models.Model):

    DEVOLUCAO = 1
    RECEBIDO = 2
    PENDENTE = 3
    RETITENSNF_TYPES = (
        (DEVOLUCAO, 'Devolução'),
        (RECEBIDO, 'Recebido'),
        (PENDENTE, 'Pendente'),
    )
    

    CHAVENFE = models.CharField(max_length=50, unique=True)

    status = models.PositiveSmallIntegerField(choices=RETITENSNF_TYPES, blank=True, null=True)
    #created_at = models.DateTimeField(editable=False)
    #updated_at = models.DateTimeField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)



    def __str__(self):
        return self.CHAVENFE
    
    class  Meta:
        ordering = ('-updated_at',)


class RetItens(models.Model):

 
    numeroNF = models.ForeignKey(RetornoItensNFEntrada, related_name='ITEMS', null=True, blank=True, on_delete=models.CASCADE)

    #DEVOLUCAO = 1
    #RECEBIDO = 2
    #PENDENTE = 3
    #RETITENS_TYPES = (
    #    (DEVOLUCAO, 'Devolução'),
    #    (RECEBIDO, 'Recebido'),
    #    (PENDENTE, 'Pendente'),
    #)
    NUMSEQ = models.IntegerField()
    CODPROD = models.CharField(max_length=20)
    QTPROD = models.IntegerField(blank=True, null=True)
    QTAVARIA = models.IntegerField(blank=True, null=True)
    QTFALTA = models.IntegerField(blank=True, null=True)
    LOTFAB = models.CharField(max_length=100, blank=True, null=True)
    NSER = models.CharField(max_length=200, blank=True, null=True)


    #DTFAB_OLD = models.DateField(blank=True, null=True)
    #DTVEN_OLD = models.DateField(blank=True, null=True)

    DTFAB = models.CharField(max_length=10, blank=True, null=True)
    DTVEN = models.CharField(max_length=10, blank=True, null=True)

    nfDev = models.CharField(max_length=15, blank=True, null=True)

    #status = models.PositiveSmallIntegerField(choices=RETITENS_TYPES, blank=True, null=True)
    observacao = models.CharField(max_length=100, blank=True, null=True )

    #created_at = models.DateTimeField(auto_now_add=True, editable=False)
    #updated_at = models.DateTimeField(auto_now=True, editable=False)


    def __str__(self):
        return self.CODPROD


 
            
