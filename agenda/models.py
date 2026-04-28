from django.db import models
from django.conf import settings
from pacientes.models import Paciente


class LugarConsulta(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del lugar')
    direccion = models.CharField(max_length=200, blank=True, verbose_name='Dirección')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono del lugar')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    orden = models.PositiveSmallIntegerField(default=0, verbose_name='Orden en listas')

    class Meta:
        verbose_name = 'Lugar de consulta'
        verbose_name_plural = 'Lugares de consulta'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('confirmada', 'Confirmada'),
        ('atendida', 'Atendida'),
        ('cancelada', 'Cancelada'),
        ('no_asistio', 'No asistió'),
    ]
    ESTADO_COLORES = {
        'programada': 'primary',
        'confirmada': 'success',
        'atendida': 'secondary',
        'cancelada': 'danger',
        'no_asistio': 'warning',
    }
    CANAL_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('ambos', 'WhatsApp y Email'),
    ]

    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE,
        related_name='citas', verbose_name='Paciente'
    )
    fecha = models.DateField(verbose_name='Fecha')
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')
    motivo = models.CharField(max_length=200, verbose_name='Motivo de la cita')
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES,
        default='programada', verbose_name='Estado'
    )
    lugar = models.ForeignKey(
        LugarConsulta, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='citas', verbose_name='Lugar de consulta'
    )
    notas = models.TextField(blank=True, verbose_name='Notas')

    # ── Recordatorio ──────────────────────────────────────────────────────────
    recordatorio_enviado = models.BooleanField(default=False, verbose_name='Recordatorio enviado')
    recordatorio_fecha = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de envío')
    recordatorio_canal = models.CharField(
        max_length=10, choices=CANAL_CHOICES,
        blank=True, verbose_name='Canal usado'
    )

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='citas_creadas', verbose_name='Creado por'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['fecha', 'hora_inicio']

    def __str__(self):
        return f'{self.paciente.nombre_completo} — {self.fecha} {self.hora_inicio}'

    def get_color(self):
        return self.ESTADO_COLORES.get(self.estado, 'secondary')

    def get_whatsapp_url(self):
        """Genera URL de WhatsApp con mensaje de recordatorio prellenado."""
        telefono = self.paciente.telefono
        telefono_limpio = telefono.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        if telefono_limpio.startswith('0'):
            telefono_limpio = '+58' + telefono_limpio[1:]
        elif not telefono_limpio.startswith('+'):
            telefono_limpio = '+58' + telefono_limpio

        lugar_str = f' en {self.lugar.nombre}' if self.lugar else ''
        nombre = self.paciente.nombre_completo.split()[0]
        mensaje = (
            f'Hola {nombre}, le recordamos su cita con {settings.CONSULTORIO_NOMBRE} '
            f'el {self.fecha.strftime("%d/%m/%Y")} a las {self.hora_inicio.strftime("%H:%M")}'
            f'{lugar_str}. Por favor confirme su asistencia. Gracias.'
        )
        import urllib.parse
        return f'https://wa.me/{telefono_limpio}?text={urllib.parse.quote(mensaje)}'

    def get_email_asunto(self):
        return f'Recordatorio de cita — {self.fecha.strftime("%d/%m/%Y")}'

    def get_email_cuerpo(self):
        lugar_str = f'\nLugar: {self.lugar.nombre}' if self.lugar else ''
        nombre = self.paciente.nombre_completo.split()[0]
        return (
            f'Estimada {nombre},\n\n'
            f'Le recordamos su cita médica con {settings.CONSULTORIO_NOMBRE}:\n\n'
            f'Fecha: {self.fecha.strftime("%d/%m/%Y")}\n'
            f'Hora: {self.hora_inicio.strftime("%H:%M")}{lugar_str}\n\n'
            f'Por favor confirme su asistencia respondiendo este mensaje.\n\n'
            f'Atentamente,\n{settings.CONSULTORIO_NOMBRE}\n{settings.CONSULTORIO_TELEFONO}'
        )
