#!/bin/bash
set -e
echo "=== Migraciones ==="
python manage.py migrate
echo "=== Archivos estaticos ==="
python manage.py collectstatic --noinput
echo "=== Creando admin ==="
python crear_admin.py
echo "=== Iniciando servidor ==="
gunicorn consultorio.wsgi --bind 0.0.0.0: --workers 2 --timeout 120