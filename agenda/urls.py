from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('', views.agenda_hoy, name='hoy'),
    path('semana/', views.agenda_semana, name='semana'),
    path('citas/nueva/', views.nueva_cita, name='cita_nueva'),
    path('citas/<int:pk>/editar/', views.editar_cita, name='cita_editar'),
    path('citas/<int:pk>/recordatorio/', views.marcar_recordatorio, name='cita_recordatorio'),
    path('<str:fecha>/', views.agenda_dia, name='dia'),
]
