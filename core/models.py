from django.db import models
from django_softdelete.models import SoftDeleteModel
from django.utils import timezone


class BaseModel(SoftDeleteModel):
    """
    Base model with full soft-delete functionality + timestamps.
    Inherit this in all app models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
