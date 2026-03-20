from django.urls import path
from .views import *

app_name = 'profissionais'

urlpatterns = [
    path('profissionais/', ProfissionalListView.as_view(), name='profissional-list'), 
    path('profissionais/edit/<int:pk>/', ProfissionalUpdateView.as_view(), name='profissional-update'), 
    path('profissionais/delete/<int:pk>/', ProfissionalDeleteView.as_view(), name='profissional-delete'), 
    path('profissionais/add/', ProfissionalCreateView.as_view(), name='profissional-create')
]