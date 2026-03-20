from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Servico
from .forms import ServicoForm

from .models import Servico
from .forms import ServicoForm


class ServicoListView(LoginRequiredMixin, ListView):
    model = Servico
    template_name = "servico_list.html"
    context_object_name = "servicos"
    paginate_by = 6
    ordering = ['preco']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '').strip()
        categoria = self.request.GET.get('categoria', '').strip()
        
        if search:
            queryset = queryset.filter(nome__icontains=search)
        
        if categoria:
            queryset = queryset.filter(categoria=categoria)

        return queryset


class ServicoCreateView(LoginRequiredMixin, CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = "servico_form.html"
    success_url = reverse_lazy('servicos:servico-list')


class ServicoUpdateView(LoginRequiredMixin, UpdateView):
    model = Servico
    form_class = ServicoForm
    template_name = "servico_form.html"
    success_url = reverse_lazy('servicos:servico-list')


class ServicoDeleteView(LoginRequiredMixin, DeleteView):
    model = Servico
    template_name = "servico_confirm_delete.html"
    success_url = reverse_lazy('servicos:servico-list')
