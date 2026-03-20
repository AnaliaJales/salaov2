from django.urls import path
from .views import *

app_name = 'relatorios'

urlpatterns = [
    path('relatorios/', RelatoriosView.as_view(), name='relatorios'), 
    path('relatorios/dados/', DadosRelatorioView.as_view(), name='dados-relatorio'),
    path('relatorios/faturamento/', DadosRelatorioFaturamentoView.as_view(), name='dados-relatorio-faturamento'),
    path('relatorios/servicos/', DadosRelatorioServicosView.as_view(), name='dados-relatorio-servicos'),
    path('relatorios/profissionais/', DadosRelatorioProfissionaisView.as_view(), name='dados-relatorio-profissionais'),
    path('relatorios/status/', DadosRelatorioStatusView.as_view(), name='dados-relatorio-status'),
    path('relatorios/clientes/', DadosRelatorioClientesView.as_view(), name='dados-relatorio-clientes'),
    path('relatorios/pdf/', RelatorioPDFView.as_view(), name='relatorio-pdf'),
]
