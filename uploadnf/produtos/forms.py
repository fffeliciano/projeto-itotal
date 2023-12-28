from django import forms

from produtos.models import Produtos

class ProdForm(forms.ModelForm):

    class Meta:
        model = Produtos
        fields = {'codprod', 'nomeprod', 'iws_erp', 'tpolret', 'iautodtven', 'qtddpzoven', 'ilotfab', 'idtfab', 'idtven', 'inser', 'codfab', 'nomefab'}
