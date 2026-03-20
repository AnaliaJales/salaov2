from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Cliente
from .forms import ClienteForm


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "cliente_list.html"
    context_object_name = "clientes"
    ordering = ['nome']
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search)
            )
        return queryset


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente_form.html"
    success_url = reverse_lazy('clientes:cliente-list')


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente_form.html"
    success_url = reverse_lazy('clientes:cliente-list')


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = "cliente_confirm_delete.html"
    success_url = reverse_lazy('clientes:cliente-list')
