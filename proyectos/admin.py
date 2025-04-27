from django.contrib import admin
from .models import Proyecto, Tarea, Bitacora

class TareaInline(admin.StackedInline):
    model = Tarea
    extra = 1  # Muestra 1 fila vacía para agregar tareas nuevas
    
class BitacoraInline(admin.TabularInline):
    model = Bitacora
    extra = 1

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'estado')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('estado',)
    ordering = ('fecha_inicio',)
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )
    inlines = [TareaInline, BitacoraInline]  # <<----- AQUÍ se agregan tareas y bitácoras dentro del proyecto

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'prioridad', 'proyecto')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('estado', 'prioridad')
    ordering = ('prioridad',)

