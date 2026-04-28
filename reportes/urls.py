from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('<int:paciente_id>/pdf/', views.generar_pdf_historial, name='pdf_historial'),
]
