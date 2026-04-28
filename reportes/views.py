from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from datetime import date
from pacientes.models import Paciente


@login_required
def generar_pdf_historial(request, paciente_id):
    if not request.user.es_doctora:
        messages.error(request, 'No tienes permiso para generar reportes.')
        return redirect('agenda:hoy')

    paciente = get_object_or_404(Paciente, pk=paciente_id)
    consultas = paciente.consultas.prefetch_related('adjuntos').order_by('fecha')

    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    import io

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()
    morado = colors.HexColor('#6f42c1')

    estilo_titulo = ParagraphStyle('titulo', parent=styles['Normal'],
        fontSize=16, fontName='Helvetica-Bold', textColor=morado, spaceAfter=4)
    estilo_subtitulo = ParagraphStyle('subtitulo', parent=styles['Normal'],
        fontSize=10, textColor=colors.grey, spaceAfter=12)
    estilo_seccion = ParagraphStyle('seccion', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica-Bold', textColor=morado,
        spaceBefore=12, spaceAfter=4, borderPad=2)
    estilo_normal = ParagraphStyle('normal_custom', parent=styles['Normal'],
        fontSize=9, spaceAfter=3)
    estilo_label = ParagraphStyle('label', parent=styles['Normal'],
        fontSize=8, textColor=colors.grey)

    elementos = []

    # ── Membrete ──────────────────────────────────────────────────────────────
    elementos.append(Paragraph(settings.CONSULTORIO_NOMBRE, estilo_titulo))
    elementos.append(Paragraph(
        f'{settings.CONSULTORIO_ESPECIALIDAD} · {settings.CONSULTORIO_TELEFONO}',
        estilo_subtitulo
    ))
    elementos.append(HRFlowable(width='100%', thickness=2, color=morado))
    elementos.append(Spacer(1, 0.3*cm))

    # ── Datos personales ──────────────────────────────────────────────────────
    elementos.append(Paragraph('HISTORIA CLÍNICA', estilo_seccion))
    datos = [
        ['Paciente:', paciente.nombre_completo, 'Cédula:', paciente.cedula],
        ['F. Nacimiento:', paciente.fecha_nacimiento.strftime('%d/%m/%Y'),
         'Edad:', f'{paciente.get_edad()} años'],
        ['Teléfono:', paciente.telefono,
         'Estado civil:', paciente.get_estado_civil_display()],
        ['Seguro:', paciente.seguro_medico or '—',
         'Ocupación:', paciente.ocupacion or '—'],
    ]
    tabla_datos = Table(datos, colWidths=[3*cm, 6*cm, 3*cm, 5*cm])
    tabla_datos.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (2, 0), (2, -1), colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla_datos)
    elementos.append(Spacer(1, 0.3*cm))

    # ── Antecedentes ──────────────────────────────────────────────────────────
    elementos.append(Paragraph('ANTECEDENTES', estilo_seccion))
    antec = []
    if paciente.alergias:
        antec.append(['Alergias:', paciente.alergias])
    if paciente.enfermedades_cronicas:
        antec.append(['Enf. crónicas:', paciente.enfermedades_cronicas])
    if paciente.medicacion_actual:
        antec.append(['Medicación:', paciente.medicacion_actual])
    if paciente.cirugias_previas:
        antec.append(['Cirugías:', paciente.cirugias_previas])

    antec_fam = []
    if paciente.antec_cancer_mama:
        antec_fam.append('Ca. mama')
    if paciente.antec_cancer_cuello:
        antec_fam.append('Ca. cuello')
    if paciente.antec_diabetes:
        antec_fam.append('Diabetes')
    if paciente.antec_hipertension:
        antec_fam.append('HTA')
    if antec_fam:
        antec.append(['Fam.:', ', '.join(antec_fam)])

    if antec:
        tabla_antec = Table(antec, colWidths=[3.5*cm, 13.5*cm])
        tabla_antec.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        elementos.append(tabla_antec)

    # ── Datos gineco-obstétricos ───────────────────────────────────────────────
    elementos.append(Paragraph('GINECO-OBSTÉTRICO', estilo_seccion))
    go_data = [
        ['Fórmula obs.:', paciente.get_formula_obstetrica(),
         'FUR:', paciente.fur.strftime('%d/%m/%Y') if paciente.fur else '—'],
        ['Citología:', paciente.ultima_citologia_fecha.strftime('%d/%m/%Y') if paciente.ultima_citologia_fecha else '—',
         'Result.:', paciente.ultima_citologia_resultado or '—'],
        ['VIH:', paciente.get_vih_resultado_display(),
         'VPH vacuna:', 'Sí' if paciente.vph_vacuna else 'No'],
        ['Método AC:', paciente.metodo_anticonceptivo or '—',
         'Menopausia:', 'Sí' if paciente.menopausia else 'No'],
    ]
    tabla_go = Table(go_data, colWidths=[3*cm, 6*cm, 3*cm, 5*cm])
    tabla_go.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (2, 0), (2, -1), colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla_go)

    # ── Consultas ─────────────────────────────────────────────────────────────
    elementos.append(Spacer(1, 0.3*cm))
    elementos.append(HRFlowable(width='100%', thickness=1, color=colors.lightgrey))
    elementos.append(Paragraph('HISTORIAL DE CONSULTAS', estilo_seccion))

    if consultas:
        for consulta in consultas:
            tipo = 'CONTROL PRENATAL' if consulta.es_prenatal else 'CONSULTA'
            elementos.append(Paragraph(
                f'<b>{consulta.fecha.strftime("%d/%m/%Y")}</b> — {tipo}',
                ParagraphStyle('ch', parent=styles['Normal'],
                    fontSize=9, fontName='Helvetica-Bold',
                    spaceBefore=8, spaceAfter=2, textColor=morado)
            ))
            elementos.append(Paragraph(
                f'<b>Motivo:</b> {consulta.motivo_consulta}', estilo_normal))
            if consulta.diagnostico:
                elementos.append(Paragraph(
                    f'<b>Diagnóstico:</b> {consulta.diagnostico}', estilo_normal))
            if consulta.tratamiento:
                elementos.append(Paragraph(
                    f'<b>Tratamiento:</b> {consulta.tratamiento}', estilo_normal))
            if consulta.observaciones:
                elementos.append(Paragraph(
                    f'<b>Obs.:</b> {consulta.observaciones}', estilo_normal))

            # Links a adjuntos
            adjuntos = consulta.adjuntos.all()
            if adjuntos:
                for adj in adjuntos:
                    elementos.append(Paragraph(
                        f'📎 <a href="{adj.get_url()}" color="blue">{adj.nombre_original}</a>',
                        estilo_normal
                    ))
    else:
        elementos.append(Paragraph('Sin consultas registradas.', estilo_normal))

    # ── Pie de página ─────────────────────────────────────────────────────────
    elementos.append(Spacer(1, 0.5*cm))
    elementos.append(HRFlowable(width='100%', thickness=1, color=colors.lightgrey))
    elementos.append(Paragraph(
        f'Generado el {date.today().strftime("%d/%m/%Y")} · {settings.CONSULTORIO_NOMBRE}',
        ParagraphStyle('pie', parent=styles['Normal'],
            fontSize=7, textColor=colors.grey, alignment=TA_CENTER, spaceBefore=6)
    ))

    doc.build(elementos)
    buffer.seek(0)

    nombre_archivo = f'historial_{paciente.cedula}_{date.today().isoformat()}.pdf'
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre_archivo}"'
    return response
