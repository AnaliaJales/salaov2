from django import forms
from .models import ProdutoEstoque

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = ProdutoEstoque
        fields = ['nome', 'categoria', 'quantidade', 'preco_custo', 'preco_venda', 'fornecedor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fornecedor': forms.TextInput(attrs={'class': 'form-control'}),
        }
