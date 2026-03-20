from django.urls import path, include
from .views import AddAgendamentoView, AgendamentoDeleteView, AgendamentoIndexView, update_agendamento_ajax

app_name = 'agendamentos'

urlpatterns = [
    path('agendamento/', AgendamentoIndexView.as_view(), name='index'),
    path('agendamento/add/', AddAgendamentoView.as_view(), name='add-agendamento'), 
    path('agendamento/update/<int:pk>/', update_agendamento_ajax, name='update-agendamento'), 
    path('agendamento/delete/<int:pk>/', AgendamentoDeleteView.as_view(), name='delete-agendamento'),
    path('calendarios/', include('apps.agendamentos.calendarios.urls')),
]
