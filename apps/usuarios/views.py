from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from core.views import AdminRequiredMixin


class UsuariosView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = "usuarios_list.html"
    context_object_name = "usuarios"

class EditUsuarioView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'is_staff']
    template_name = "edit_usuarios.html"
    success_url = reverse_lazy('usuarios:usuarios')

    def get_form_class(self):
        form_class = super().get_form_class()
        if self.get_object().is_superuser:
            from django import forms
            class SuperuserForm(form_class):
                is_staff = forms.BooleanField(disabled=True, required=False)
            return SuperuserForm
        return form_class

class DeleteUsuarioView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    context_object_name = 'usuario'
    template_name = "usuarios_confirm_delete.html"
    success_url = reverse_lazy('usuarios:usuarios')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_superuser:
            context = self.get_context_data(delete_error=True)
            return self.render_to_response(context)
        return super().post(request, *args, **kwargs)

class RegisterView(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        # user vai pro grupo "Recepcionista"
        recepcionista_group = Group.objects.get_or_create(name='Recepcionista')[0]
        user.groups.add(recepcionista_group)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_obj'] = self.request.user
        return ctx
