from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pacientes.models import Paciente
from agenda.models import Cita
from .models import Consulta, AdjuntoConsulta
from .forms import ConsultaForm


@login_required
def nueva_consulta(request, paciente_id):
    if not request.user.es_doctora:
        messages.error(request, 'No tienes permiso para registrar consultas.')
        return redirect('agenda:hoy')

    paciente = get_object_or_404(Paciente, pk=paciente_id)

    # Cita asociada (opcional — viene del botón en agenda)
    cita_id = request.GET.get('cita')
    cita = None
    if cita_id:
        cita = get_object_or_404(Cita, pk=cita_id)

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente
            if cita:
                consulta.cita = cita
                # Marcar cita como atendida
                cita.estado = 'atendida'
                cita.save()
            consulta.save()
            messages.success(request, 'Consulta registrada correctamente.')
            return redirect('pacientes:detalle', pk=paciente.pk)
    else:
        from datetime import date
        initial = {'fecha': date.today()}
        # Heredar lugar de la cita si existe
        if cita and cita.lugar:
            initial['lugar'] = cita.lugar
        form = ConsultaForm(initial=initial)

    return render(request, 'consultas/form.html', {
        'form': form,
        'paciente': paciente,
        'cita': cita,
        'titulo': 'Nueva consulta',
    })


@login_required
def detalle_consulta(request, pk):
    if not request.user.es_doctora:
        messages.error(request, 'No tienes permiso para ver consultas.')
        return redirect('agenda:hoy')

    consulta = get_object_or_404(
        Consulta.objects.select_related('paciente', 'lugar').prefetch_related('adjuntos'),
        pk=pk
    )
    return render(request, 'consultas/detalle.html', {'consulta': consulta})


@login_required
def adjuntar_archivo(request, pk):
    if not request.user.es_doctora:
        messages.error(request, 'No tienes permiso para adjuntar archivos.')
        return redirect('agenda:hoy')

    consulta = get_object_or_404(Consulta, pk=pk)
    from .forms import AdjuntoForm
    if request.method == 'POST':
        form = AdjuntoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES.get('archivo')
            if archivo:
                from consultas.drive import subir_archivo_drive
                try:
                    resultado = subir_archivo_drive(archivo, consulta)
                    AdjuntoConsulta.objects.create(
                        consulta=consulta,
                        drive_file_id=resultado['file_id'],
                        nombre_original=archivo.name,
                        tipo='imagen' if archivo.content_type.startswith('image') else 'pdf',
                        drive_folder_id=resultado.get('folder_id', ''),
                    )
                    messages.success(request, f'Archivo "{archivo.name}" subido correctamente.')
                except Exception as e:
                    messages.error(request, f'Error al subir archivo: {e}')
            return redirect('pacientes:detalle', pk=consulta.paciente.pk)
    else:
        form = AdjuntoForm()

    return render(request, 'consultas/adjuntar.html', {'form': form, 'consulta': consulta})
