from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class AgendaView(LoginRequiredMixin, TemplateView):
    template_name = 'calendarios/agenda.html'


    def get_context_data(self, **kwargs):
        from apps.profissionais.models import Profissional
        from apps.agendamentos.models import Agendamento
        from datetime import date
        context = super().get_context_data(**kwargs)
        

        date_str = self.request.GET.get('date', date.today().isoformat())
        try:
            agenda_date = date.fromisoformat(date_str)
        except ValueError:
            agenda_date = date.today()
        
        profissionais = Profissional.objects.filter(
            agendamento__data_hora__date=agenda_date
        ).distinct().order_by('nome')
        context['profissionais'] = profissionais

        
        agendamentos_today = Agendamento.objects.filter(
            data_hora__date=agenda_date
        ).select_related('cliente', 'servico', 'profissional').order_by('profissional__nome', 'data_hora')
        
# Flatten and group by horario for multiple appearances per professional
        from collections import defaultdict
        horario_groups = defaultdict(list)
        for ag in agendamentos_today:
            horario_str = ag.data_hora.time().strftime('%H:%M')
            horario_groups[horario_str].append(ag)
        
        # For each horario, sort professionals alphabetically
        agenda_list = []
        for horario_str in sorted(horario_groups.keys()):
            prof_groups = defaultdict(list)
            for ag in horario_groups[horario_str]:
                prof_groups[ag.profissional.id].append(ag)
            
            for prof_id, ags in sorted(prof_groups.items(), key=lambda x: x[1][0].profissional.nome):
                prof = profissionais.get(id=prof_id)
                if prof:
                    agenda_list.append({
                        'horario_str': horario_str,
                        'profissional': prof,
                        'agendamentos': ags
                    })
        
        context['agenda_list'] = agenda_list
        context['agenda_date'] = agenda_date
        context['date_str'] = date_str
        return context