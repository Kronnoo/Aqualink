from django.db import models
from django.contrib.auth.models import User

class Nivel(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    codigo = models.CharField(max_length=11, unique=True, editable=False)
    nombre = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=80)
    fecha_nacimiento = models.DateField()
    nivel = models.ForeignKey(Nivel, on_delete=models.PROTECT)
    tutor_nombre = models.CharField(max_length=100)
    tutor_telefono = models.CharField(max_length=15)
    fecha_alta = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'alumno'
        ordering = ['apellidos', 'nombre']

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = 'AQ-' + secrets.token_hex(4).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.alumno} - {self.fecha}"

class Tiempo(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='tiempos')
    prueba = models.CharField(max_length=100)
    segundos = models.FloatField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.alumno} - {self.prueba}: {self.segundos}s"

class Incidente(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='incidentes')
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField()
    accion_tomada = models.TextField()

    def __str__(self):
        return f"Incidente {self.alumno} ({self.fecha})"
