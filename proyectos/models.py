from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='perfiles/', default='perfiles/default.jpg')
    
    def __str__(self):
        return f'Perfil de {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#Modulo de Proyecto, Tarea y Bitacora
class Proyecto(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),    # Para proyectos que aún no inician
        ('Activo', 'Activo'),         # Para proyectos en curso
        ('Finalizado', 'Finalizado')   # Para proyectos completados
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    
    def save(self, *args, **kwargs):
        # Solo validamos que si está finalizado tenga fecha de fin
        if self.estado == 'Finalizado' and not self.fecha_fin:
            self.fecha_fin = datetime.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
class Tarea(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('En Progreso', 'En Progreso'), ('Completada', 'Completada')])
    prioridad = models.IntegerField()
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_asignadas', db_column='asignado_a')

    def __str__(self):
        return f"{self.nombre} ({self.estado})"

class Bitacora(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='bitacoras')
    fecha = models.DateField()
    comentario = models.TextField()
    avance = models.IntegerField(help_text="Porcentaje de avance del proyecto")
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='bitacoras_escritas')

    def __str__(self):
        return f"{self.fecha} - {self.avance}%"
