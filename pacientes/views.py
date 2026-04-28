from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Paciente
from .forms import PacientePersonalForm, PacienteCompletoForm


@login_required
def lista_pacientes(request):
    q = request.GET.get('q', '').strip()
    pacientes = Paciente.objects.all()
    if q:
        pacientes = pacientes.filter(
            Q(nombre_completo__icontains=q) | Q(cedula__icontains=q) | Q(telefono__icontains=q)
        )
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes, 'q': q})


@login_required
def nueva_paciente(request):
    if request.method == 'POST':
        form = PacienteCompletoForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, f'Paciente {paciente.nombre_completo} registrada correctamente.')
            return redirect('pacientes:detalle', pk=paciente.pk)
    else:
        form = PacienteCompletoForm()
    return render(request, 'pacientes/form.html', {'form': form, 'titulo': 'Nueva paciente'})


@login_required
def detalle_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    consultas = paciente.consultas.all().prefetch_related('adjuntos')
    citas = paciente.citas.order_by('-fecha', '-hora_inicio')[:10]
    return render(request, 'pacientes/detalle.html', {
        'paciente': paciente,
        'consultas': consultas,
        'citas': citas,
    })


@login_required
def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    # Asistente solo puede editar datos personales
    if request.user.es_asistente:
        FormClass = PacientePersonalForm
    else:
        FormClass = PacienteCompletoForm

    if request.method == 'POST':
        form = FormClass(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ficha actualizada correctamente.')
            return redirect('pacientes:detalle', pk=paciente.pk)
    else:
        form = FormClass(instance=paciente)

    return render(request, 'pacientes/form.html', {
        'form': form,
        'paciente': paciente,
        'titulo': 'Editar ficha',
    })
