from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('welcome')),

    # Páginas generales
    path('welcome/', views.welcome, name='welcome'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/index2/', views.index2_view, name='index2'),
    path('dashboard/index3/', views.index3_view, name='index3'),

    # Registro
    path('register/', views.register, name='register'),

    # Recuperación de contraseña con pregunta secreta
    path('recuperar-password/', views.recuperar_password_view, name='recuperar_password'),
    path('verificar-respuesta/', views.verificar_respuesta_view, name='verificar_respuesta'),
    path('nueva-password/', views.nueva_password_view, name='nueva_password'),
]
