import io
import qrcode
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db.models import Min

from .models import Alumno, Asistencia, Tiempo
from .forms import TiempoForm

# --- FASE 6: PASAPORTE INTELIGENTE ---

@login_required
def qr_nadador(request, codigo):
    alumno = get_object_or_404(Alumno, codigo=codigo)
    url = request.build_absolute_uri(reverse('pasaporte', args=[alumno.codigo]))
    imagen = qrcode.make(url)
    buffer = io.BytesIO()
    imagen.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')

def pasaporte(request, codigo):
    alumno = get_object_or_404(Alumno, codigo=codigo, activo=True)
    asistencias = alumno.asistencias.order_by('-fecha')
    contexto = {
        'alumno': alumno,
        'asistencias': asistencias[:10],
        'total': asistencias.count(),
        'ya_registrada': asistencias.filter(fecha=timezone.localdate()).exists(),
    }
    return render(request, 'nadadores/pasaporte.html', contexto)

@login_required
@require_POST
def registrar_asistencia(request, codigo):
    alumno = get_object_or_404(Alumno, codigo=codigo, activo=True)
    asistencia, creada = Asistencia.objects.get_or_create(
        alumno=alumno,
        fecha=timezone.localdate(),
        defaults={'registrada_por': request.user.username},
    )
    if creada:
        messages.success(request, f'Asistencia de {alumno.nombre} registrada.')
    else:
        messages.info(request, f'{alumno.nombre} ya tenía asistencia hoy.')
    return redirect('pasaporte', codigo=alumno.codigo)

# --- FASE 7: PANEL DEPORTIVO Y REGISTRO DE TIEMPOS ---

@login_required
@require_POST
def registrar_tiempo(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    form = TiempoForm(request.POST)
    if form.is_valid():
        tiempo = form.save(commit=False)
        tiempo.alumno = alumno
        tiempo.save()
        messages.success(request, 'Tiempo registrado.')
    else:
        messages.error(request, 'Revisa los datos: el tiempo debe ser mayor que 0.')
    return redirect('perfil_nadador', alumno_id=alumno.id)

@login_required
def panel(request):
    hoy = timezone.localdate()
    pruebas = Tiempo.objects.values_list('prueba', flat=True).distinct().order_by('prueba')
    prueba = request.GET.get('prueba') or '25 m libre'
    filas = []
    
    alumnos = Alumno.objects.filter(activo=True, tiempos__prueba=prueba).distinct()
    for alumno in alumnos:
        marcas = alumno.tiempos.filter(prueba=prueba).order_by('fecha')
        primero = marcas.first().segundos
        ultimo = marcas.last().segundos
        mejor = marcas.aggregate(Min('segundos'))['segundos__min']
        mejora = round((primero - mejor) / primero * 100, 1)
        filas.append({
            'alumno': alumno,
            'registros': marcas.count(),
            'primero': primero,
            'mejor': mejor,
            'ultimo': ultimo,
            'mejora': mejora,
        })
        
    filas.sort(key=lambda f: f['mejor'])
    mayor_mejora = max([f['mejora'] for f in filas], default=0)
    for f in filas:
        f['ancho'] = int(f['mejora'] / mayor_mejora * 100) if mayor_mejora else 0
        
    promedio = round(sum(f['mejora'] for f in filas) / len(filas), 1) if filas else 0
    
    contexto = {
        'pruebas': pruebas,
        'prueba': prueba,
        'filas': filas,
        'total_activos': Alumno.objects.filter(activo=True).count(),
        'asistencias_mes': Asistencia.objects.filter(
            fecha__year=hoy.year, fecha__month=hoy.month).count(),
        'mejor_marca': filas[0] if filas else None,
        'promedio_mejora': promedio,
    }
    return render(request, 'nadadores/panel.html', contexto)