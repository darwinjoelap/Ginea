from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cita
from pacientes.models import Paciente


@login_required
def agenda_hoy(request):
    return agenda_dia(request, fecha=date.today().isoformat())


@login_required
def agenda_dia(request, fecha):
    try:
        fecha_obj = date.fromisoformat(fecha)
    except ValueError:
        fecha_obj = date.today()

    citas = Cita.objects.filter(fecha=fecha_obj).select_related('paciente', 'creado_por')

    # Días anterior y siguiente para navegación
    dia_anterior = (fecha_obj - timedelta(days=1)).isoformat()
    dia_siguiente = (fecha_obj + timedelta(days=1)).isoformat()

    # Resumen por estado
    resumen = {
        'total': citas.count(),
        'atendidas': citas.filter(estado='atendida').count(),
        'pendientes': citas.filter(estado__in=['programada', 'confirmada']).count(),
        'canceladas': citas.filter(estado__in=['cancelada', 'no_asistio']).count(),
    }

    context = {
        'fecha': fecha_obj,
        'citas': citas,
        'dia_anterior': dia_anterior,
        'dia_siguiente': dia_siguiente,
        'es_hoy': fecha_obj == date.today(),
        'resumen': resumen,
    }
    return render(request, 'agenda/dia.html', context)


@login_required
def agenda_semana(request):
    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    dias = []
    for i in range(6):  # lunes a sábado
        dia = inicio_semana + timedelta(days=i)
        citas = Cita.objects.filter(fecha=dia).select_related('paciente')
        dias.append({'fecha': dia, 'citas': citas})

    context = {
        'dias': dias,
        'semana_anterior': (inicio_semana - timedelta(days=7)).isoformat(),
        'semana_siguiente': (inicio_semana + timedelta(days=7)).isoformat(),
    }
    return render(request, 'agenda/semana.html', context)


@login_required
def nueva_cita(request):
    from .forms import CitaForm
    paciente_id = request.GET.get('paciente')
    fecha_inicial = request.GET.get('fecha', date.today().isoformat())

    initial = {'fecha': fecha_inicial}
    paciente = None
    if paciente_id:
        paciente = get_object_or_404(Paciente, pk=paciente_id)
        initial['paciente'] = paciente

    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.creado_por = request.user
            cita.save()
            messages.success(request, f'Cita agendada para {cita.paciente.nombre_completo}.')
            return redirect('agenda:dia', fecha=cita.fecha.isoformat())
    else:
        form = CitaForm(initial=initial)

    return render(request, 'agenda/cita_form.html', {
        'form': form,
        'paciente': paciente,
        'titulo': 'Nueva cita',
    })


@login_required
def editar_cita(request, pk):
    from .forms import CitaForm
    cita = get_object_or_404(Cita, pk=pk)

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada.')
            return redirect('agenda:dia', fecha=cita.fecha.isoformat())
    else:
        form = CitaForm(instance=cita)

    return render(request, 'agenda/cita_form.html', {
        'form': form,
        'cita': cita,
        'titulo': 'Editar cita',
    })


import json
from django.http import JsonResponse
from django.utils import timezone


@login_required
def marcar_recordatorio(request, pk):
    """Vista AJAX — marca una cita como recordatorio enviado."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    cita = get_object_or_404(Cita, pk=pk)
    try:
        data = json.loads(request.body)
        canal = data.get('canal', 'whatsapp')
    except Exception:
        canal = 'whatsapp'

    cita.recordatorio_enviado = True
    cita.recordatorio_fecha = timezone.now()
    cita.recordatorio_canal = canal
    cita.save(update_fields=['recordatorio_enviado', 'recordatorio_fecha', 'recordatorio_canal'])

    return JsonResponse({'ok': True})
