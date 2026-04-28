git add Procfile
git commit -m "Fix Procfile con collectstatic y crear admin"
git push origin mainweb: python manage.py migrate && python manage.py collectstatic --noinput && python crear_admin.py && gunicorn consultorio.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 120