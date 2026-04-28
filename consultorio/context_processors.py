from django.conf import settings


def consultorio_info(request):
    """Inyecta datos del consultorio en todos los templates."""
    return {
        'CONSULTORIO_NOMBRE': settings.CONSULTORIO_NOMBRE,
        'CONSULTORIO_ESPECIALIDAD': settings.CONSULTORIO_ESPECIALIDAD,
        'CONSULTORIO_TELEFONO': settings.CONSULTORIO_TELEFONO,
    }
