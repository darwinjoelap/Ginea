from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('agenda/', include('agenda.urls')),
    path('consultas/', include('consultas.urls')),
    path('reportes/', include('reportes.urls')),
    # Raíz → agenda del día
    path('', RedirectView.as_view(url='/agenda/', permanent=False)),
]
