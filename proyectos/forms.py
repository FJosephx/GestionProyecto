from django import forms
from .models import Proyecto, Tarea, Bitacora
from django.contrib.auth.models import User


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        estado = cleaned_data.get('estado')

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise forms.ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')

        if estado == 'Finalizado' and not fecha_fin:
            raise forms.ValidationError('Un proyecto finalizado debe tener fecha de fin.')

        return cleaned_data


class TareaForm(forms.ModelForm):
    asignado_a = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        empty_label="Seleccione un usuario",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Tarea
        fields = ['nombre', 'descripcion', 'estado', 'prioridad', 'asignado_a']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(choices=[(1, '1 - Alta'), (2, '2 - Media'), (3, '3 - Baja')], attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TareaForm, self).__init__(*args, **kwargs)
        self.fields['asignado_a'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}" if obj.first_name else obj.username


class BitacoraForm(forms.ModelForm):
    class Meta:
        model = Bitacora
        fields = ['fecha', 'comentario', 'avance']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'avance': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
        }
