from django.contrib import admin

# Register your models here.
from .models import Produtos, Embalagens


admin.site.register(Produtos)
admin.site.register(Embalagens)