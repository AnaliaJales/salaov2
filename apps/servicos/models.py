from django.db import models
from django_softdelete.models import SoftDeleteModel
from core.models import BaseModel


class Servico(BaseModel):
    CATEGORIA_CHOICES = [
        ('CABELO', 'Cabelo'),
        ('MAQUIAGEM', 'Maquiagem'),
        ('SPA', 'Spa'),
        ('UNHAS', 'Unhas'),
        ('BARBA', 'Barba'),
        ('DEPILACAO', 'Depilação'),
        ('MASSAGEM', 'Massagem'),
        ('SOBRANCELHAS', 'Sobrancelhas'),
        ('CILIOS', 'Cílios'),
    ]

    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='CABELO'
    )

    def __str__(self):
        return self.nome

