from ast import parse

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Profissional
from .forms import ProfissionalForm
from core.views import RecepcionistaRequiredMixin


class ProfissionalListView(LoginRequiredMixin, RecepcionistaRequiredMixin, ListView):
    model = Profissional
    template_name = "profissional_list.html"
    context_object_name = "profissionais"
    paginate_by = 6
    ordering = ['nome']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(especialidade__icontains=search)
            )
        return queryset

    

class ProfissionalCreateView(LoginRequiredMixin, RecepcionistaRequiredMixin, CreateView):
    model = Profissional
    form_class = ProfissionalForm
    template_name = "profissional_form.html"
    success_url = reverse_lazy('profissionais:profissional-list')


class ProfissionalUpdateView(LoginRequiredMixin, RecepcionistaRequiredMixin, UpdateView):
    model = Profissional
    form_class = ProfissionalForm
    template_name = "profissional_form.html"
    success_url = reverse_lazy('profissionais:profissional-list')


class ProfissionalDeleteView(LoginRequiredMixin, RecepcionistaRequiredMixin, DeleteView):
    model = Profissional
    template_name = "profissional_confirm_delete.html"
    success_url = reverse_lazy('profissionais:profissional-list')
