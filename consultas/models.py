from django.db import models
from pacientes.models import Paciente
from agenda.models import Cita


class Consulta(models.Model):
    lugar = models.ForeignKey(
        'agenda.LugarConsulta', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='consultas', verbose_name='Lugar de consulta'
    )
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE,
        related_name='consultas', verbose_name='Paciente'
    )
    cita = models.OneToOneField(
        Cita, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='consulta', verbose_name='Cita asociada'
    )
    fecha = models.DateField(verbose_name='Fecha de consulta')

    # ── Datos clínicos ────────────────────────────────────────────────────────
    motivo_consulta = models.TextField(verbose_name='Motivo de consulta')
    sintomas_actuales = models.TextField(verbose_name='Síntomas actuales', blank=True)
    examen_fisico = models.TextField(verbose_name='Examen físico', blank=True)
    diagnostico = models.TextField(verbose_name='Diagnóstico')
    tratamiento = models.TextField(verbose_name='Tratamiento')
    proxima_cita = models.DateField(null=True, blank=True, verbose_name='Próxima cita')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')

    # ── Signos vitales ────────────────────────────────────────────────────────
    peso = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name='Peso (kg)'
    )
    tension_arterial = models.CharField(
        max_length=20, blank=True, verbose_name='Tensión arterial',
        help_text='Ej: 120/80'
    )

    # ── Control prenatal ──────────────────────────────────────────────────────
    es_prenatal = models.BooleanField(default=False, verbose_name='Es control prenatal')
    fpp = models.DateField(
        null=True, blank=True, verbose_name='FPP (Fecha probable de parto)'
    )
    semanas_gestacion = models.IntegerField(
        null=True, blank=True, verbose_name='Semanas de gestación'
    )
    altura_uterina = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True,
        verbose_name='Altura uterina (cm)'
    )
    fcf = models.IntegerField(
        null=True, blank=True,
        verbose_name='FCF (Frecuencia cardíaca fetal, lpm)'
    )
    presentacion_fetal = models.CharField(
        max_length=50, blank=True, verbose_name='Presentación fetal'
    )
    edemas = models.BooleanField(null=True, blank=True, verbose_name='Edemas')

    # ── Control ───────────────────────────────────────────────────────────────
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-fecha', '-creado_en']

    def __str__(self):
        tipo = 'Prenatal' if self.es_prenatal else 'Consulta'
        return f'{tipo} — {self.paciente.nombre_completo} ({self.fecha})'


class AdjuntoConsulta(models.Model):
    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('pdf', 'PDF'),
    ]

    consulta = models.ForeignKey(
        Consulta, on_delete=models.CASCADE,
        related_name='adjuntos', verbose_name='Consulta'
    )
    drive_file_id = models.CharField(max_length=100, verbose_name='ID de archivo en Drive')
    nombre_original = models.CharField(max_length=255, verbose_name='Nombre del archivo')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name='Tipo')
    drive_folder_id = models.CharField(
        max_length=100, blank=True, verbose_name='ID de carpeta en Drive'
    )
    subido_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Adjunto'
        verbose_name_plural = 'Adjuntos'
        ordering = ['subido_en']

    def __str__(self):
        return f'{self.nombre_original} ({self.consulta})'

    def get_url(self):
        return f'https://drive.google.com/file/d/{self.drive_file_id}/view'

    def get_thumbnail_url(self):
        """URL de miniatura para imágenes en Drive."""
        return f'https://drive.google.com/thumbnail?id={self.drive_file_id}&sz=w300'
