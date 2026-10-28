from django import forms
from .models import Alumno, Tiempo

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