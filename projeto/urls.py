#import padrão
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import logout
# extras
from django.contrib.auth import views as auth_views
from core.views import HomeView

def logout_view(request):
    """Clear the session and redirect to login."""
    logout(request)
    return redirect('login')
 
urlpatterns = [
    # core
    path('', HomeView.as_view(), name='home'),
    path('index/', lambda request: redirect('agendamentos:index'), name='index'),
    
    # obrigatorias
    path('admin/', admin.site.urls),

    # register
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),

    #cruds urls
    path('agendamentos/', include('apps.agendamentos.urls', namespace='agendamentos')),
    path('agenda/', include('apps.agendamentos.calendarios.urls'), name='agenda'),
    path('clientes/', include('apps.clientes.urls', namespace='clientes')),
    path('profissionais/', include('apps.profissionais.urls', namespace='profissionais')),
    path('servicos/', include('apps.servicos.urls', namespace='servicos')),
    path('usuarios/', include('apps.usuarios.urls', namespace='usuarios')),
    path('relatorios/', include('apps.relatorios.urls', namespace='relatorios')),
    path('estoque/', include('estoque.urls', namespace='estoque')),
]
