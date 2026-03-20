from django.urls import path
from .views import (
    EstoqueListView, EstoqueCreateView, 
    EstoqueUpdateView, EstoqueDeleteView
)

app_name = 'estoque'

urlpatterns = [
    path('', EstoqueListView.as_view(), name='estoque-list'),
    path('add/', EstoqueCreateView.as_view(), name='estoque-create'),
    path('edit/<int:pk>/', EstoqueUpdateView.as_view(), name='estoque-update'),
    path('delete/<int:pk>/', EstoqueDeleteView.as_view(), name='estoque-delete'),
]
