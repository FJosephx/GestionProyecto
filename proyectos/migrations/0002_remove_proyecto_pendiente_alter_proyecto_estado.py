# Generated by Django 5.2 on 2025-05-01 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='pendiente',
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Activo', 'Activo'), ('Finalizado', 'Finalizado')], default='Pendiente', max_length=20),
        ),
    ]
