"""
Django settings para el consultorio ginecológico.
"""
from pathlib import Path
from decouple import config, Csv

# ─────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────
# Seguridad
# ─────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='django-insecure-cambia-esto-en-produccion')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,ginea-production.up.railway.app', cast=Csv())

# ─────────────────────────────────────────────
# Apps instaladas
# ─────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'crispy_forms',
    'crispy_bootstrap5',

    # Propias
    'accounts',
    'pacientes',
    'agenda',
    'consultas',
    'reportes',
]

# ─────────────────────────────────────────────
# Middleware
# ─────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',       # sirve estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'consultorio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Datos del consultorio disponibles en todos los templates
                'consultorio.context_processors.consultorio_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'consultorio.wsgi.application'

# ─────────────────────────────────────────────
# Base de datos
# ─────────────────────────────────────────────
_db_url = config('DATABASE_URL', default='')

if _db_url:
    # PostgreSQL en producción
    import dj_database_url
    DATABASES = {'default': dj_database_url.parse(_db_url)}
else:
    # SQLite en desarrollo
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ─────────────────────────────────────────────
# Autenticación
# ─────────────────────────────────────────────
AUTH_USER_MODEL = 'accounts.Usuario'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# ─────────────────────────────────────────────
# Internacionalización
# ─────────────────────────────────────────────
LANGUAGE_CODE = 'es-ve'
TIME_ZONE = 'America/Caracas'
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────
# Archivos estáticos
# ─────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ─────────────────────────────────────────────
# Google Drive
# ─────────────────────────────────────────────
GOOGLE_DRIVE_CREDENTIALS_FILE = config(
    'GOOGLE_DRIVE_CREDENTIALS_FILE',
    default=str(BASE_DIR / 'credentials.json')
)
GOOGLE_DRIVE_ROOT_FOLDER_NAME = config(
    'GOOGLE_DRIVE_ROOT_FOLDER_NAME',
    default='Consultorio Ginecologico'
)

# ─────────────────────────────────────────────
# Datos del consultorio (para PDFs y templates)
# ─────────────────────────────────────────────
CONSULTORIO_NOMBRE = config('CONSULTORIO_NOMBRE', default='Dra. Ana Martinez')
CONSULTORIO_ESPECIALIDAD = config('CONSULTORIO_ESPECIALIDAD', default='Ginecología y Obstetricia')
CONSULTORIO_TELEFONO = config('CONSULTORIO_TELEFONO', default='+58 412-000-0000')

# ─────────────────────────────────────────────
# Crispy Forms
# ─────────────────────────────────────────────
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# ─────────────────────────────────────────────
# Misc
# ─────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
