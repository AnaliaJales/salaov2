from django import forms
from .models import *

from django.utils import timezone
from django.core.exceptions import ValidationError


class AgendamentoForm(forms.ModelForm):

    class Meta:
        model = Agendamento
        fields = '__all__'
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.localtime()
        
        self.fields['data_hora'].widget.attrs['min'] = now.strftime('%Y-%m-%dT%H:%M')
        
        # especialidade
        self.fields['profissional'].label_from_instance = lambda obj: f"{obj.nome} ({obj.especialidade})"

    def clean_data_hora(self):
        data = self.cleaned_data.get('data_hora')
        if data and data < timezone.now():
            raise ValidationError('A data e hora não podem ser anteriores ao momento atual.')
        
        if data:
            agendamentos_existentes = Agendamento.objects.filter(
                data_hora=data,
                status__in=['AGENDADO', 'CONCLUIDO']
            )
            if self.instance.pk:
                agendamentos_existentes = agendamentos_existentes.exclude(pk=self.instance.pk)
            
            if agendamentos_existentes.exists():
                raise ValidationError('Já existe um agendamento agendado para este horário.')
        
        return data

    def save(self, commit=True):
        obj = super().save(commit=False)
        if obj.data_hora and obj.data_hora <= timezone.now() and obj.status == 'AGENDADO':
            obj.status = 'CONCLUIDO'
        if commit:
            obj.save()
        return obj