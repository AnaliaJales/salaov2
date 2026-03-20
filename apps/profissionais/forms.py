from django import forms
from .models import *


class ProfissionalForm(forms.ModelForm):
    class Meta:
        model = Profissional
        fields = ('__all__')