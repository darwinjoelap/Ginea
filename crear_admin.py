import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consultorio.settings')
import django
django.setup()
from accounts.models import Usuario
if not Usuario.objects.filter(username='admin').exists():
    Usuario.objects.create_superuser(
        username='admin',
        password='CambiarEsto2024!',
        rol='doctora',
        first_name='Vanessa',
        last_name='Pereira',
    )
    print('Superusuario creado')
else:
    print('Ya existe')
