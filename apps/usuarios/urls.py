from django.urls import path
from .views import *
from projeto.urls import *

app_name = 'usuarios'

urlpatterns = [
    path('usuarios/', UsuariosView.as_view(), name='usuarios'), 
    path('usuarios/edit/<int:pk>/', EditUsuarioView.as_view(), name='edit-usuario'),
    path('usuarios/delete/<int:pk>/', DeleteUsuarioView.as_view(), name='delete-usuario'),
    path('perfil/', ProfileView.as_view(), name='perfil'),
    path('register/', RegisterView.as_view(), name='register')
]