from django.contrib import admin
 
#Register your models here.
from fornecedor.models import NotasFiscais, Itens, Sku, RetornoItensNFEntrada, RetItens

class SkuAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nomeProduto', 'ean')
    list_filter = ('nomeProduto','updated_at')


class NotasFiscaisAdmin(admin.ModelAdmin):
    list_display = ('nNF', 'xNome_emit' ,'vNF')
    list_filter = ('status','xNome_emit')

admin.site.register(NotasFiscais, NotasFiscaisAdmin)

admin.site.register(RetornoItensNFEntrada)
admin.site.register(RetItens)


admin.site.register(Itens)

admin.site.register(Sku, SkuAdmin)


