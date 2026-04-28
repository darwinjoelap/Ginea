from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'email', 'rol', 'is_active')
    list_filter = ('rol', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Rol en el consultorio', {'fields': ('rol',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol en el consultorio', {'fields': ('rol',)}),
    )
