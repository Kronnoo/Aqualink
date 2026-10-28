from django.contrib import admin
from .models import Nivel, Alumno, Asistencia, Tiempo, Evaluacion, Incidente

# Personaliza cómo se ven los alumnos en el panel de control
@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'apellidos', 'nivel', 'activo') # Columnas a ver
    search_fields = ('nombre', 'apellidos', 'codigo')                  # Buscador
    list_filter = ('nivel', 'activo')                                  # Filtros

# Registra los demás modelos para poder administrarlos
admin.site.register([Nivel, Asistencia, Tiempo, Evaluacion, Incidente])