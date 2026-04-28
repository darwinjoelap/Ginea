from django.urls import path
from . import views

app_name = 'consultas'

urlpatterns = [
    path('nueva/<int:paciente_id>/', views.nueva_consulta, name='nueva'),
    path('<int:pk>/', views.detalle_consulta, name='detalle'),
    path('<int:pk>/adjuntar/', views.adjuntar_archivo, name='adjuntar'),
]
