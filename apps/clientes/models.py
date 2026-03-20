from django.db import models
from django_softdelete.models import SoftDeleteModel
from core.models import BaseModel


class Cliente(BaseModel):
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

