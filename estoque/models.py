from django.db import models
from django_softdelete.models import SoftDeleteModel
from core.models import BaseModel


class ProdutoEstoque(BaseModel):
    CATEGORIA_CHOICES = [
        ('CABELO', 'Produtos para Cabelo'),
        ('TINTAS', 'Tintas e Colorações'),
        ('UNHAS', 'Produtos para Unhas'),
        ('MAQUIAGEM', 'Maquiagem'),
        ('SPA', 'Spa e Tratamentos'),
        ('DEPILACAO', 'Depilação'),
        ('SOBRANCELHAS', 'Sobrancelhas e Cílios'),
    ]

    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='CABELO')
    quantidade = models.PositiveIntegerField(default=0)
    preco_custo = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    preco_venda = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fornecedor = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.categoria}"

    @property
    def total_custo(self):
        return self.quantidade * self.preco_custo

    @property 
    def total_venda(self):
        return self.quantidade * self.preco_venda
