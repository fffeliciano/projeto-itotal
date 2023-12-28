from django.db import models
from datetime import datetime


class Estoque(models.Model):
    
    #status = models.CharField(max_length=10)
    #nome_atualizacao = models.CharField(max_length=50)
    nome_atualizacao = models.CharField(max_length=50)

    #status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
       
    def __str__(self):
        return self.nome_atualizacao

    class Meta:
        ordering = ('-id',)


class Itens(models.Model):
    
    idestoque = models.ForeignKey(Estoque,related_name='itens', on_delete=models.CASCADE)

    #nome_atualizacao = models.CharField(max_length=50, primary_key=True )
    #nome_atualizacao = models.CharField(max_length=30, primary_key=True )
     
    cd = models.CharField(max_length=30)
    ft = models.PositiveIntegerField()
    qc = models.PositiveIntegerField()
    qb = models.PositiveIntegerField()
    qf = models.PositiveIntegerField()

    def __str__(self):
        return self.cd