from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Agendamento
from apps.clientes.models import Cliente
from apps.profissionais.models import Profissional
from apps.servicos.models import Servico
from .forms import AgendamentoForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime
import json


from core.views import RecepcionistaRequiredMixin

class AgendamentoIndexView(RecepcionistaRequiredMixin, ListView):
    model = Agendamento
    paginate_by = 4
    template_name = 'index.html'
    context_object_name = 'agendamentos'

    def get_queryset(self):
        Agendamento.atualizar_statuss()
        queryset = Agendamento.objects.select_related(
            'cliente', 'servico', 'profissional'
        )

        # Filters from GET params
        if self.request.GET.get('profissional'):
            queryset = queryset.filter(profissional__id=self.request.GET.get('profissional'))
        if self.request.GET.get('cliente'):
            queryset = queryset.filter(cliente__id=self.request.GET.get('cliente'))
        if self.request.GET.get('servico'):
            queryset = queryset.filter(servico__id=self.request.GET.get('servico'))
        if self.request.GET.get('data'):
            from datetime import date
            try:
                filter_date = date.fromisoformat(self.request.GET.get('data'))
                queryset = queryset.filter(data_hora__date=filter_date)
            except ValueError:
                pass
        if self.request.GET.get('hora'):
            try:
                hora_str = self.request.GET.get('hora')
                if len(hora_str) >= 2:
                    hora_int = int(hora_str[:2])
                    from datetime import time
                    start_time = time(hora_int, 0)
                    end_time = time(hora_int + 1, 0) if hora_int < 23 else time(23, 59)
                    queryset = queryset.filter(
                        data_hora__time__gte=start_time,
                        data_hora__time__lt=end_time
                    )
            except ValueError:
                pass
        if self.request.GET.get('status'):
            queryset = queryset.filter(status=self.request.GET.get('status'))
        if self.request.GET.get('agendamento_id'):
            queryset = queryset.filter(id=self.request.GET.get('agendamento_id'))

        return queryset.order_by('-data_hora')
    
    def get_context_data(self, **kwargs):
        from apps.clientes.models import Cliente
        from apps.servicos.models import Servico
        from apps.profissionais.models import Profissional
        context = super().get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.all()
        context['servicos'] = Servico.objects.all()
        context['profissionais'] = Profissional.objects.all()
        
        # Check if viewing single agendamento
        single_qs = self.object_list if hasattr(self, 'object_list') else self.get_queryset()
        context['single_agendamento'] = single_qs.exists() and single_qs.count() == 1
        return context

    ordering = ['-data_hora']


class AddAgendamentoView(LoginRequiredMixin, CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'add_agendamentos.html'
    success_url = reverse_lazy('index')


class AgendamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Agendamento
    template_name = 'agendamento_confirm_delete.html'
    success_url = reverse_lazy('index')

@csrf_exempt
@require_http_methods(["POST"])
def update_agendamento_ajax(request, pk):
    """AJAX endpoint for inline agendamento editing"""
    try:
        agendamento = Agendamento.objects.get(pk=pk)
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Agendamento atualizado com sucesso!',
                'data': {
                    'cliente': str(form.instance.cliente),
                    'servico': form.instance.servico.nome,
                    'profissional': form.instance.profissional.nome,
                    'data_hora': form.instance.data_hora.strftime('%d/%m/%Y às %H:%M'),
                    'status': form.instance.get_status_display(),
                    'status_class': form.instance.status.lower(),
                    'observacoes': form.instance.observacoes or ''
                }
            })
        else:
            return JsonResponse({'success': False, 'message': form.errors}, status=400)
    except Agendamento.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Agendamento não encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
