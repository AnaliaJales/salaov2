from django.contrib import admin
# from django_softdelete.admin import SoftDeleteAdminMixin
from .models import ProdutoEstoque

@admin.register(ProdutoEstoque)
class ProdutoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'quantidade', 'preco_custo', 'preco_venda', 'total_custo']
    list_filter = ['categoria']
    search_fields = ['nome', 'fornecedor']
    
    def total_custo(self, obj):
        return f"R$ {obj.quantidade * obj.preco_custo:.2f}"
    total_custo.short_description = 'Total Custo'
