from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Usuario del sistema. Extiende AbstractUser con un campo de rol.
    """
    ROL_DOCTORA = 'doctora'
    ROL_ASISTENTE = 'asistente'
    ROL_CHOICES = [
        (ROL_DOCTORA, 'Doctora'),
        (ROL_ASISTENTE, 'Asistente'),
    ]

    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default=ROL_ASISTENTE,
        verbose_name='Rol',
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_rol_display()})'

    @property
    def es_doctora(self):
        return self.rol == self.ROL_DOCTORA

    @property
    def es_asistente(self):
        return self.rol == self.ROL_ASISTENTE
