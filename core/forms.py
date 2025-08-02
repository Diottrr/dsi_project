from django import forms
from django.contrib.auth.models import User
from .models import Perfil


class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    pregunta_secreta = forms.CharField(
        label="Pregunta secreta",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    respuesta_secreta = forms.CharField(
        label="Respuesta secreta",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Perfil.objects.update_or_create(
                user=user,
                defaults={
                    'pregunta_secreta': self.cleaned_data['pregunta_secreta'].strip(),
                    'respuesta_secreta': self.cleaned_data['respuesta_secreta'].strip().lower()
                }
            )
        return user


class RecuperarPasswordUsuarioForm(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class VerificarRespuestaForm(forms.Form):
    respuesta = forms.CharField(
        label='Respuesta secreta',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class NuevaPasswordForm(forms.Form):
    nueva_password = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
