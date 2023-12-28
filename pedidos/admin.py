from django.contrib import admin

# Register your models here.
from .models import Pedidos, Itens, Embarque, NotasFiscaisSaida, ItensNF
#from .models import Pedidos, Itens, NotasFiscaisSaida, ItensNF, EmbarqueFour

admin.site.register(Pedidos)

admin.site.register(Itens)

admin.site.register(Embarque)


admin.site.register(NotasFiscaisSaida)
admin.site.register(ItensNF)
