from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Alumno, Tiempo


class LoginForm(AuthenticationForm):
    """Login con placeholders y clases para poder darle estilo."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'campo', 'placeholder': 'Usuario', 'autofocus': True})
        self.fields['password'].widget.attrs.update(
            {'class': 'campo', 'placeholder': 'Contraseña'})


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellidos', 'fecha_nacimiento', 'nivel',
                  'tutor_nombre', 'tutor_telefono']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }


class UsuarioForm(UserCreationForm):
    """Alta de personal (solo superusuario)."""
    pass


class TiempoForm(forms.ModelForm):
    class Meta:
        model = Tiempo
        fields = ['prueba', 'segundos', 'fecha']
        labels = {'segundos': 'Tiempo (segundos)'}
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean_segundos(self):
        segundos = self.cleaned_data['segundos']
        if segundos <= 0:
            raise forms.ValidationError('El tiempo debe ser mayor que 0.')
        return segundos