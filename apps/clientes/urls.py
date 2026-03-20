from django.urls import path
from .views import *

app_name = 'clientes'

urlpatterns = [
    path('clientes/', ClienteListView.as_view(), name='cliente-list'), 
    path('clientes/add/', ClienteCreateView.as_view(), name='cliente-create'), 
    path('clientes/edit/<int:pk>/', ClienteUpdateView.as_view(), name='cliente-update'), 
    path('clientes/delete/<int:pk>/', ClienteDeleteView.as_view(), name='cliente-delete')
]