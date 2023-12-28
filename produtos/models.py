from django.db import models
from datetime import datetime, timezone

class Produtos(models.Model):
    
    codprod = models.CharField(max_length=30, primary_key=True )
    nomeprod = models.CharField(max_length=100)
    #codprod = models.CharField(max_length=20, unique=True )
    iws_erp = models.CharField(max_length=1, blank=True)
    tpolret = models.CharField(max_length=1, default=1)
    iautodtven = models.CharField(max_length=1, default=0)
    qtddpzoven = models.CharField(max_length=1, default=1)
    ilotfab = models.CharField(max_length=1, default=0)
    idtfab = models.CharField(max_length=1, default=0)
    idtven = models.CharField(max_length=1, default=0)
    inser = models.CharField(max_length=1, default=1)
    #codfab = models.CharField(max_length=20)
    codfab = models.CharField(max_length=20, blank=True)
    nomefab = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self):
        return self.nomeprod

    class Meta:
        ordering = ('-codprod',)

class Embalagens(models.Model):
    
    idprod = models.ForeignKey(Produtos, related_name='embalagens',on_delete=models.CASCADE)

    codunid = models.CharField(max_length=20, default="un")
    fator = models.CharField(max_length=8)
    codbarra = models.CharField(max_length=30)
    pesoliq = models.DecimalField(max_digits=10, decimal_places=3)
    #pesoliq = models.CharField(max_length=12)
    pesobru = models.DecimalField(max_digits=10, decimal_places=3)
    #pesobru = models.CharField(max_length=12)

    alt = models.IntegerField()
    lar = models.IntegerField()
    comp = models.IntegerField()
    vol = models.CharField(max_length=20)
    
    #alt = models.CharField(max_length=12, blank=True)
    #lar = models.CharField(max_length=12, blank=True)
    #comp = models.CharField(max_length=12, blank=True)
    #vol = models.CharField(max_length=12, default="1", blank=True)
    
    #iemb_ent = models.CharField(max_length=10)
    #iemb_sai = models.CharField(max_length=10)

    def __str__(self):
        return self.codbarra
    
    
