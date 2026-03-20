from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, Count, F, Q
from django.core.exceptions import PermissionDenied
from .models import ProdutoEstoque
from .forms import EstoqueForm

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    def handle_no_permission(self):
        raise PermissionDenied("Acesso restrito ao administrador/dono.")

class EstoqueListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = ProdutoEstoque
    template_name = "estoque_list.html"
    context_object_name = "estoques"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '').strip()
        categoria = self.request.GET.get('categoria', '').strip()
        
        if search:
            queryset = queryset.filter(Q(nome__icontains=search) | Q(fornecedor__icontains=search))
        
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        
        context['total_estoque'] = qs.aggregate(total=Count('id'))['total'] or 0
        context['total_custo'] = qs.aggregate(total=Sum(F('quantidade') * F('preco_custo')))['total'] or 0
        context['total_venda'] = qs.aggregate(total=Sum(F('quantidade') * F('preco_venda')))['total'] or 0
        context['categorias'] = ProdutoEstoque.CATEGORIA_CHOICES
        context['search'] = self.request.GET.get('search', '')
        context['categoria'] = self.request.GET.get('categoria', '')
        
        return context

class EstoqueCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = ProdutoEstoque
    form_class = EstoqueForm
    template_name = "estoque_form.html"
    success_url = reverse_lazy('estoque:estoque-list')

class EstoqueUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = ProdutoEstoque
    form_class = EstoqueForm
    template_name = "estoque_form.html"
    success_url = reverse_lazy('estoque:estoque-list')

class EstoqueDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = ProdutoEstoque
    template_name = "estoque_confirm_delete.html"
    success_url = reverse_lazy('estoque:estoque-list')
