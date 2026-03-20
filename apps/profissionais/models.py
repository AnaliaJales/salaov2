from django.db import models
from django_softdelete.models import SoftDeleteModel
from core.models import BaseModel


class Profissional(BaseModel):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


