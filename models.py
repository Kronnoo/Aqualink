import secrets
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Tabla de niveles de natación
class Nivel(models.Model):
    orden = models.PositiveSmallIntegerField(unique=True)
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False  # Django no crea ni modifica esta tabla, ya existe en MySQL
        db_table = 'nivel'
        ordering = ['orden']

    def __str__(self):
        return self.nombre

# Tabla de nadadores/alumnos
class Alumno(models.Model):
    codigo = models.CharField(max_length=11, unique=True, editable=False)
    nombre = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=80)
    fecha_nacimiento = models.DateField()
    nivel = models.ForeignKey(Nivel, on_delete=models.PROTECT) # Relación con Nivel
    tutor_nombre = models.CharField(max_length=100)
    tutor_telefono = models.CharField(max_length=15)
    fecha_alta = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'alumno'
        ordering = ['apellidos', 'nombre']

    # Al guardar un alumno nuevo, le genera un código único como 'AQ-7F3A91C2'
    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = 'AQ-' + secrets.token_hex(4).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'

# Tabla para registrar asistencias
class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField()
    registrada_por = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'asistencia'
        unique_together = ('alumno', 'fecha')

# Tabla para guardar tiempos de pruebas
class Tiempo(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='tiempos')
    prueba = models.CharField(max_length=30)
    segundos = models.DecimalField(max_digits=6, decimal_places=2)
    fecha = models.DateField()

    class Meta:
        managed = False
        db_table = 'tiempo'

# Tabla para evaluaciones de los alumnos
class Evaluacion(models.Model):
    AREAS = [
        ('Tecnica', 'Técnica'),
        ('Seguridad acuatica', 'Seguridad acuática'),
        ('Desarrollo humano', 'Desarrollo humano'),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='evaluaciones')
    fecha = models.DateField()
    area = models.CharField(max_length=20, choices=AREAS)
    puntaje = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]) # Nota entre 1 y 10
    observacion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evaluacion'

# Tabla para registrar incidentes médicos
class Incidente(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='incidentes')
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    accion_tomada = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'incidente'