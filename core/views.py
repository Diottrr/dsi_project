from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistroForm

from .forms import (
    RegistroForm,
    RecuperarPasswordUsuarioForm,
    VerificarRespuestaForm,
    NuevaPasswordForm
)
from .models import Perfil

# VISTA DE BIENVENIDA
def welcome(request):
    return render(request, 'welcome.html')

# DASHBOARD (requiere login)
@login_required
def dashboard_view(request):
    return render(request, 'index.html')

def index2_view(request):
    return render(request, 'index2.html')

def index3_view(request):
    return render(request, 'index3.html')

# REGISTRO CON PREGUNTA SECRETA

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()  # Aquí ya crea usuario y perfil
            print("Usuario registrado con éxito")
            return redirect('welcome')
        else:
            print("Formulario inválido", form.errors)
    else:
        form = RegistroForm()
    return render(request, 'registration/register.html', {'form': form})




# VISTA 1: Ingresar usuario
def recuperar_password_view(request):
    if request.method == 'POST':
        form = RecuperarPasswordUsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                perfil = user.perfil
                request.session['recuperar_user_id'] = user.id
                return render(request, 'registration/verificar_pregunta.html', {
                    'pregunta': perfil.pregunta_secreta,
                    'form': VerificarRespuestaForm()
                })
            except User.DoesNotExist:
                form.add_error('username', 'Usuario no encontrado')
    else:
        form = RecuperarPasswordUsuarioForm()
    return render(request, 'registration/recuperar_password.html', {'form': form})

# VISTA 2: Verificar respuesta secreta
def verificar_respuesta_view(request):
    user_id = request.session.get('recuperar_user_id')
    if not user_id:
        return redirect('password_reset_custom')
    user = get_object_or_404(User, id=user_id)
    perfil = user.perfil

    if request.method == 'POST':
        form = VerificarRespuestaForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['respuesta'].strip().lower() == perfil.respuesta_secreta.strip().lower():
                # Respuesta correcta, redirigir a la página de nueva contraseña
                return redirect('nueva_password')
            else:
                form.add_error('respuesta', 'Respuesta incorrecta')
    else:
        form = VerificarRespuestaForm()

    return render(request, 'registration/verificar_pregunta.html', {
        'pregunta': perfil.pregunta_secreta,
        'form': form
    })

# VISTA 3: Ingresar nueva contraseña
def nueva_password_view(request):
    user_id = request.session.get('recuperar_user_id')
    if not user_id:
        return redirect('recuperar_password')
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = NuevaPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['nueva_password'])
            user.save()
            del request.session['recuperar_user_id']
            # Al cambiar la contraseña redirige a confirmación
            return render(request, 'registration/password_cambiada.html')
    else:
        form = NuevaPasswordForm()

    # Aquí muestra el formulario para ingresar nueva contraseña
    return render(request, 'registration/nueva_password.html', {'form': form})
