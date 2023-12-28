from django.contrib import admin

# Register your models here.
from .models import Estoque, Itens


admin.site.register(Estoque)
admin.site.register(Itens)


 