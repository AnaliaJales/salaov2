# padrao
from django.db import models
from django.utils import timezone
from django_softdelete.models import SoftDeleteModel
from core.models import BaseModel

#models externos
from apps.clientes.models import Cliente
from apps.profissionais.models import Profissional
from apps.servicos.models import Servico


class Agendamento(BaseModel):

    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        indexes = [
            models.Index(fields=['status', 'data_hora']),
        ]

    def __str__(self):
        return f"{self.cliente} - {self.servico}"

    @classmethod
    def atualizar_statuss(cls):
        cls.objects.filter(status='AGENDADO', data_hora__lte=timezone.now()).update(status='CONCLUIDO')

    def clean(self):
        from django.core.exceptions import ValidationError

        # bloqueio horário
        if self.data_hora:
            hora = self.data_hora.time().hour
            if hora < 9 or hora >= 22:
                raise ValidationError({'data_hora': 'Agendamentos só são permitidos entre 9h e 22h.'})
        
        # Validação de duplicatas existente
        agendamentos_existentes = Agendamento.objects.filter(
            data_hora=self.data_hora,
            status__in=['AGENDADO', 'CONCLUIDO']
        )
        
        if self.pk:
            agendamentos_existentes = agendamentos_existentes.exclude(pk=self.pk)
        
        if agendamentos_existentes.exists():
            raise ValidationError({'data_hora': 'Já existe um agendamento agendado para este horário.'})

    def save(self, *args, **kwargs):
        self.full_clean()  #executa as validações do clean()
        if self.data_hora and self.data_hora <= timezone.now() and self.status == 'AGENDADO':
            self.status = 'CONCLUIDO'
        super().save(*args, **kwargs)
