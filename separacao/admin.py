from django.contrib import admin

from separacao.models import  Separacao, ItensSeparacao

#class Separacao(admin.ModelAdmin):
#    list_display = ('numpedcli', 'qtvol', 'status')
#    list_filter = ('numpedcli','updated_at')


admin.site.register(Separacao)
admin.site.register(ItensSeparacao)


