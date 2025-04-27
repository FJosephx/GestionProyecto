from django.db import models

#Modulo de Proyecto, Tarea y Bitacora
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[('Activo', 'Activo'), ('Finalizado', 'Finalizado')])

    def __str__(self):
        return self.nombre
    
class Tarea(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('En Progreso', 'En Progreso'), ('Completada', 'Completada')])
    prioridad = models.IntegerField()
    asignado_a = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.estado})"

class Bitacora(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='bitacoras')
    fecha = models.DateField()
    comentario = models.TextField()
    avance = models.IntegerField(help_text="Porcentaje de avance del proyecto")

    def __str__(self):
        return f"{self.fecha} - {self.avance}%"
