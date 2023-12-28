
from django.db import models
from datetime import datetime
from inventario import settings


class Separacao(models.Model):

   


    NUMPEDCLI = models.CharField(max_length=50, unique=True)
    CGCCLIWMS = models.PositiveBigIntegerField(default=38317322000131)
    CGCEMINF = models.PositiveBigIntegerField(default=38317322000131)
    #especie = models.CharField(max_length=50)
    #pesovol = models.DecimalField(max_digits=10, decimal_places=3)
    QTVOL = models.CharField(max_length=10, blank=True, null=True)
    CGCTRANSP = models.CharField(max_length=14, blank=True, null=True)
    #DTFIMCHECK = models.DateField()
    DTFIMCHECK = models.CharField(max_length=10, blank=True, null=True)
    URLRAST = models.CharField(max_length=30, blank=True, null=True)

    #status = models.CharField(max_length=10)
    #created_at = models.DateTimeField(auto_now_add=True, editable=False)
    #updated_at = models.DateTimeField(auto_now=True, editable=False)
       
    def __str__(self):
        return self.NUMPEDCLI


    class Meta:
        ordering = ('-NUMPEDCLI',)



class ItensSeparacao(models.Model):
    ENVIADO = 1
    AGUARDANDO = 2
    PENDENTE = 3
    SEPARACAO_TYPES = (
        (ENVIADO, 'Enviado'),
        (AGUARDANDO, 'Aguardando'),
        (PENDENTE, 'Pendente'),
    )


    nItens = models.ForeignKey(Separacao,related_name='ITENS', on_delete=models.CASCADE)
   # numeroNF = models.ForeignKey(RetornoItensNFEntrada, related_name='ITEMS', null=True, blank=True, on_delete=models.CASCADE)

    NUMSEQ = models.IntegerField()
    CODPROD = models.CharField(max_length=20)
    QTPROD = models.CharField(max_length=10, blank=True, null=True)
    QTCONF = models.CharField(max_length=10, blank=True, null=True)
    LOTFAB = models.CharField(max_length=100, blank=True, null=True)
    DTFAB = models.CharField(max_length=10, blank=True, null=True)
    DTVEN = models.CharField(max_length=10, blank=True, null=True)
    #nser = models.CharField(max_length=100)

    status = models.PositiveSmallIntegerField(choices=SEPARACAO_TYPES, blank=True, null=True)
    observacao = models.CharField(max_length=100, blank=True, null=True )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


    #date_birth = forms.DateFwidget=forms.SelectDateWidget(years=YEAR_CHOICES, input_formats= DATE_INPUT_FORMATS)ield(label='Date of birth', )


    def __str__(self):
        return self.CODPROD
