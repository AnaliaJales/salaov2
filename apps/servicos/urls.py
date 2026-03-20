from django.urls import path
from .views import *

app_name = 'servicos'

urlpatterns = [
    path('servicos/', ServicoListView.as_view(), name='servico-list'), 
    path('servicos/add/', ServicoCreateView.as_view(), name='servico-create'), 
    path('servicos/edit/<int:pk>/', ServicoUpdateView.as_view(), name='servico-update'), 
    path('servicos/delete/<int:pk>/', ServicoDeleteView.as_view(), name='servico-delete')
]