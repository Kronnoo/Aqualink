from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('alumnos/', views.inicio, name='alumnos'),
    path('login/', auth_views.LoginView.as_view(
        template_name='nadadores/login.html',
        authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('nadador/nuevo/', views.registrar_nadador, name='registrar_nadador'),
    path('nadador/<int:alumno_id>/', views.perfil_nadador, name='perfil_nadador'),
    path('nadador/<int:alumno_id>/tiempo/', views.registrar_tiempo, name='registrar_tiempo'),
    path('usuarios/nuevo/', views.registrar_usuario, name='registrar_usuario'),
    path('panel/', views.panel, name='panel'),
    path('pasaporte/<str:codigo>/', views.pasaporte, name='pasaporte'),
    path('pasaporte/<str:codigo>/asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('pasaporte/<str:codigo>/qr/', views.qr_nadador, name='qr_nadador'),
]