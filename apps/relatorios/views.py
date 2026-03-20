from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek
from datetime import datetime
from django.shortcuts import render
from dateutil.parser import parse
from apps.clientes.models import Cliente 
from core.views import AdminRequiredMixin
from apps.agendamentos.models import Agendamento
from .utils.pdf_generator import generate_relatorio_pdf


class RelatoriosView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = "relatorios.html"

class RelatorioPDFView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        
        if data_inicio:
            try:
                data_inicio = parse(data_inicio).date()
            except:
                data_inicio = None
        if data_fim:
            try:
                data_fim = parse(data_fim).date()
            except:
                data_fim = None
        
        pdf_buffer = generate_relatorio_pdf(data_inicio, data_fim)
        

        # nomeação do relatorio
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="relatorio_completo_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
        response.write(pdf_buffer.getvalue())
        pdf_buffer.close()
        
        return response


class DadosRelatorioView(LoginRequiredMixin, AdminRequiredMixin, View):
    #definição filtro relatorio por dias
    def get(self, request):
        Agendamento.atualizar_statuss()

        data_inicio = parse_date(request.GET.get('data_inicio'))
        data_fim = parse_date(request.GET.get('data_fim'))

        agendamentos = Agendamento.objects.filter(status='CONCLUIDO')

        if data_inicio:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

        if data_fim:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

        total = agendamentos.count()

        por_dia = (
            agendamentos
            .annotate(dia=TruncDay('data_hora'))
            .values('dia')
            .annotate(total=Count('id'))
            .order_by('dia')
        )

        total_clientes = Cliente.objects.distinct().count()
        total_faturamento = agendamentos.aggregate(
            total=Sum('servico__preco')
        )['total'] or 0

        return JsonResponse({
            'total': total,
            'total_clientes': total_clientes,
            'total_agendamentos_abertos': Agendamento.objects.filter(status='AGENDADO').count(),
            'total_faturamento': float(total_faturamento),
            'por_dia': {
                str(item['dia'].date()): item['total']
                for item in por_dia
            }
        })


class DadosRelatorioFaturamentoView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        Agendamento.atualizar_statuss()

        data_inicio = parse_date(request.GET.get('data_inicio'))
        data_fim = parse_date(request.GET.get('data_fim'))
        periodo = request.GET.get('periodo', 'dia')

        agendamentos = Agendamento.objects.filter(status='CONCLUIDO').select_related('servico')

        if data_inicio:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

        if data_fim:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

        total_faturamento = agendamentos.aggregate(
            total=Sum('servico__preco')
        )['total'] or 0

        # Agrupamento por período
        if periodo == 'semana':
            trunc = TruncWeek
        elif periodo == 'mes':
            trunc = TruncMonth
        else:
            trunc = TruncDay

        por_periodo = (
            agendamentos
            .annotate(periodo=trunc('data_hora'))
            .values('periodo')
            .annotate(
                total=Sum('servico__preco'),
                quantidade=Count('id')
            )
            .order_by('periodo')
        )
        dados = {
                str(item['periodo'].date()): {
                'total': float(item['total'] or 0),
                'quantidade': item['quantidade']
            }
            for item in por_periodo
        }

        return JsonResponse({
            'total_faturamento': float(total_faturamento),
            'por_periodo': dados
        })
    
class DadosRelatorioServicosView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Most popular services report"""

    def get(self, request):
        Agendamento.atualizar_statuss()

        data_inicio = parse_date(request.GET.get('data_inicio'))
        data_fim = parse_date(request.GET.get('data_fim'))

        agendamentos = Agendamento.objects.filter(status='CONCLUIDO').select_related('servico')

        if data_inicio:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

        if data_fim:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

        por_servico = (
            agendamentos
            .values('servico__nome', 'servico__preco')
            .annotate(
                quantidade=Count('id'),
                total_faturado=Sum('servico__preco')
            )
            .order_by('-quantidade')
        )

        return JsonResponse({
            'servicos': [
                {
                    'nome': item['servico__nome'],
                    'preco': float(item['servico__preco']),
                    'quantidade': item['quantidade'],
                    'total_faturado': float(item['total_faturado'] or 0)
                }
                for item in por_servico
            ]
        })


class DadosRelatorioProfissionaisView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Professionals performance report"""

    def get(self, request):
        Agendamento.atualizar_statuss()

        data_inicio = parse_date(request.GET.get('data_inicio'))
        data_fim = parse_date(request.GET.get('data_fim'))

        agendamentos = Agendamento.objects.filter(status='CONCLUIDO').select_related('profissional', 'servico')

        if data_inicio:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

        if data_fim:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

        por_profissional = (
            agendamentos
            .values('profissional__nome', 'profissional__especialidade')
            .annotate(
                quantidade=Count('id'),
                total_faturado=Sum('servico__preco')
            )
            .order_by('-quantidade')
        )

        return JsonResponse({
            'profissionais': [
                {
                    'nome': item['profissional__nome'],
                    'especialidade': item['profissional__especialidade'],
                    'quantidade': item['quantidade'],
                    'total_faturado': float(item['total_faturado'] or 0)
                }
                for item in por_profissional
            ]
        })


class DadosRelatorioStatusView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Appointments by status report"""

    def get(self, request):
        Agendamento.atualizar_statuss()

        data_inicio = parse_date(request.GET.get('data_inicio'))
        data_fim = parse_date(request.GET.get('data_fim'))

        agendamentos = Agendamento.objects.all()

        if data_inicio:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

        if data_fim:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

        por_status = (
            agendamentos
            .values('status')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        return JsonResponse({
            'status': [
                {
                    'status': item['status'],
                    'total': item['total']
                }
                for item in por_status
            ],
            'total_geral': agendamentos.count()
        })


class DadosRelatorioClientesView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Top clients report"""

    def get(self, request):
        Agendamento.atualizar_statuss()

        data_inicio = parse_date(request.GET.get('data_inicio'))
        data_fim = parse_date(request.GET.get('data_fim'))

        agendamentos = Agendamento.objects.filter(status='CONCLUIDO').select_related('cliente', 'servico')

        if data_inicio:
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

        if data_fim:
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

        por_cliente = (
            agendamentos
            .values('cliente__nome', 'cliente__telefone')
            .annotate(
                quantidade=Count('id'),
                total_gasto=Sum('servico__preco')
            )
            .order_by('-total_gasto')[:10]  # Top 10 clients
        )

        return JsonResponse({
            'clientes': [
                {
                    'nome': item['cliente__nome'],
                    'telefone': item['cliente__telefone'],
                    'quantidade': item['quantidade'],
                    'total_gasto': float(item['total_gasto'] or 0)
                }
                for item in por_cliente
            ]
        })


def parse_date(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None
    return None
