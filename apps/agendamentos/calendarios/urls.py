from django.urls import path
from . import views

app_name = 'calendarios'

urlpatterns = [
    path('agenda/', views.AgendaView.as_view(), name='agenda'),
]

