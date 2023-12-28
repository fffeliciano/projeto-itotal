from django import forms

from .models import RetornoItensNFEntrada


#class RetItensForm(forms.ModelForm):
#    class Meta:
#        model = RetItens
#        fields = ('nfDev', 'observacao')



class RetornoItensNFEntradaForm(forms.ModelForm):
    class Meta:
        model = RetornoItensNFEntrada
        fields = ('CHAVENFE', 'status')
