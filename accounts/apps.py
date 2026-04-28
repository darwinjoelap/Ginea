from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Cuentas de usuario'

    def ready(self):
        import os
        if os.environ.get('DJANGO_SUPERUSER_USERNAME'):
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
                password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
                email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(
                        username=username,
                        password=password,
                        email=email,
                        rol='doctora',
                        first_name='Vanessa',
                        last_name='Pereira',
                    )
            except Exception:
                pass