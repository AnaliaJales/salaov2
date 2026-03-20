from django.contrib import admin
from .models import Servico

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco']
    list_filter = ['categoria']
    search_fields = ['nome']
