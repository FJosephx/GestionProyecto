from django import forms
from .models import Proyecto, Tarea, Bitacora


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'fecha_inicio': forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'fecha_fin': forms.TextInput(attrs={'class': 'form-control datepicker'}),
        }


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre', 'descripcion', 'estado', 'prioridad', 'asignado_a']
        widgets = {
            'fecha_inicio': forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'fecha_fin': forms.TextInput(attrs={'class': 'form-control datepicker'}),
        }

class BitacoraForm(forms.ModelForm):
    class Meta:
        model = Bitacora
        fields = ['fecha', 'comentario', 'avance']
        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'form-control datepicker'}),
        }
