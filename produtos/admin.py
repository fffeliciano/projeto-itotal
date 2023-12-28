from django.contrib import admin
 
#Register your models here.
from .models import Produtos, Embalagens


# admin.site.register(Produtos)
#admin.site.register(Embalagens)


class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('nomeprod', 'codprod' ,'nomefab')
    list_filter = ('status','nomefab')

admin.site.register(Produtos,ProdutosAdmin)

admin.site.register(Embalagens)