from django import forms
from .models import *
from decimal import Decimal


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'preco', 'categoria']
        widgets = {
            'preco': forms.TextInput(attrs={'class': 'money'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        if args:
            data = args[0]
        else:
            data = kwargs.get('data')

        if data and 'preco' in data:
            preco_val = data.get('preco', '')
            if preco_val:
                # mascara padrão do preço
                preco_val = preco_val.replace('R$', '').replace(',', '.').replace('.', '', -1)
                data = data.copy()
                data['preco'] = preco_val
                if args:
                    args = (data,) + args[1:]
                else:
                    kwargs['data'] = data
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            display_preco = str(self.instance.preco.quantize(Decimal('1')))
            self.initial['preco'] = display_preco

    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if isinstance(preco, str):
            # update de preço
            preco = preco.replace('R$', '').replace(',', '.').replace('.', '', -1)
        return preco
