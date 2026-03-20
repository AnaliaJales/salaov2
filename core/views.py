from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class HomeView(TemplateView):
    template_name = 'home.html'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        from django.shortcuts import render
        return render(self.request, '403.html', status=403)


class RecepcionistaRequiredMixin(UserPassesTestMixin):
    """Mixin that allows only users in 'Recepcionista' group or admin users"""
    
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        # Allow admin users (staff or superuser)
        if user.is_staff or user.is_superuser:
            return True
        # Check if user is in Recepcionista group
        return user.groups.filter(name='Recepcionista').exists()
    
    def handle_no_permission(self):
        from django.shortcuts import render
        return render(self.request, '403.html', status=403)
