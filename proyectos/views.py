from django.shortcuts import render, get_object_or_404, redirect
from .models import Proyecto, Tarea, Bitacora, Profile
from .forms import ProyectoForm, TareaForm, BitacoraForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.files.storage import FileSystemStorage
import json
from datetime import datetime, timedelta
from django.db.models import Count

# Vista de home
@login_required
def home(request):
    query = request.GET.get('q')
    if query:
        proyectos = Proyecto.objects.filter(nombre__icontains=query)
    else:
        proyectos = Proyecto.objects.all()

    proyectos_activos = Proyecto.objects.filter(estado='Activo').count()
    proyectos_finalizados = Proyecto.objects.filter(estado='Finalizado').count()
    tareas_totales = Tarea.objects.count()
    tareas_completadas = Tarea.objects.filter(estado='Completada').count()
    tareas_pendientes = tareas_totales - tareas_completadas

    bitacoras = Bitacora.objects.all()
    if bitacoras.exists():
        avance_promedio = round(sum([b.avance for b in bitacoras]) / bitacoras.count(), 2)
    else:
        avance_promedio = 0


    context = {
        'proyectos': proyectos,
        'proyectos_activos': proyectos_activos,
        'proyectos_finalizados': proyectos_finalizados,
        'tareas_totales': tareas_totales,
        'tareas_completadas': tareas_completadas,
        'tareas_pendientes': tareas_pendientes,
        'avance_promedio': avance_promedio,
    }
    return render(request, 'proyectos/home.html', context)


# Vista de detalle de un proyecto
@login_required
def proyecto_detail(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    tareas = proyecto.tareas.all()
    bitacoras = proyecto.bitacoras.all().order_by('fecha')  # Ordenar por fecha ascendente
    return render(request, 'proyectos/proyecto_detail.html', {
        'proyecto': proyecto,
        'tareas': tareas,
        'bitacoras': bitacoras
    })

# Crear proyecto
@login_required
def proyecto_create(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto creado exitosamente.')
            return redirect('home')
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/proyecto_form.html', {'form': form})

# Editar proyecto
@login_required
def proyecto_update(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto actualizado correctamente.')
            return redirect('home')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'proyectos/proyecto_form.html', {'form': form})

# Eliminar proyecto
@login_required
def proyecto_delete(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, 'Proyecto eliminado correctamente.')
        return redirect('home')
    return render(request, 'proyectos/proyecto_confirm_delete.html', {'proyecto': proyecto})

# Crear tarea
@login_required
def tarea_create(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.proyecto = proyecto
            tarea.save()
            messages.success(request, 'Tarea agregada correctamente.')
            return redirect('proyecto_detail', proyecto_id=proyecto.id)
    else:
        form = TareaForm()
    return render(request, 'proyectos/tarea_form.html', {'form': form, 'proyecto': proyecto})

# Editar tarea
@login_required
def tarea_update(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada correctamente.')
            return redirect('proyecto_detail', proyecto_id=tarea.proyecto.id)
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'proyectos/tarea_form.html', {'form': form, 'proyecto': tarea.proyecto})

# Eliminar tarea
@login_required
def tarea_delete(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    proyecto_id = tarea.proyecto.id
    if request.method == 'POST':
        tarea.delete()
        messages.success(request, 'Tarea eliminada correctamente.')
        return redirect('proyecto_detail', proyecto_id=proyecto_id)
    return render(request, 'proyectos/tarea_confirm_delete.html', {'tarea': tarea})

# Crear bitácora
@login_required
def bitacora_create(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = BitacoraForm(request.POST)
        if form.is_valid():
            try:
                # Obtener el último ID de bitácora
                ultimo_id = Bitacora.objects.order_by('-id').first()
                nuevo_id = (ultimo_id.id + 1) if ultimo_id else 1
                
                # Crear la bitácora manualmente
                bitacora = Bitacora(
                    id=nuevo_id,
                    fecha=form.cleaned_data['fecha'],
                    comentario=form.cleaned_data['comentario'],
                    avance=form.cleaned_data['avance'],
                    proyecto=proyecto,
                    autor=request.user  # Siempre usar el usuario actual como autor
                )
                bitacora.save()
                messages.success(request, 'Registro de bitácora agregado correctamente.')
                return redirect('proyecto_detail', proyecto_id=proyecto.id)
            except Exception as e:
                messages.error(request, f'Error al guardar la bitácora: {str(e)}')
                return render(request, 'proyectos/bitacora_form.html', {'form': form, 'proyecto': proyecto, 'bitacora': None})
    else:
        form = BitacoraForm()
    return render(request, 'proyectos/bitacora_form.html', {'form': form, 'proyecto': proyecto, 'bitacora': None})

# Editar bitácora
@login_required
def bitacora_update(request, bitacora_id):
    bitacora = get_object_or_404(Bitacora, id=bitacora_id)
    if request.method == 'POST':
        form = BitacoraForm(request.POST, instance=bitacora)
        if form.is_valid():
            try:
                # Mantener el autor original al actualizar
                bitacora = form.save(commit=False)
                bitacora.save()
                messages.success(request, 'Registro de bitácora actualizado correctamente.')
                return redirect('proyecto_detail', proyecto_id=bitacora.proyecto.id)
            except Exception as e:
                messages.error(request, f'Error al actualizar la bitácora: {str(e)}')
                return render(request, 'proyectos/bitacora_form.html', {'form': form, 'proyecto': bitacora.proyecto, 'bitacora': bitacora})
    else:
        form = BitacoraForm(instance=bitacora)
    return render(request, 'proyectos/bitacora_form.html', {'form': form, 'proyecto': bitacora.proyecto, 'bitacora': bitacora})

# Eliminar bitácora
@login_required
def bitacora_delete(request, bitacora_id):
    bitacora = get_object_or_404(Bitacora, id=bitacora_id)
    proyecto_id = bitacora.proyecto.id
    if request.method == 'POST':
        bitacora.delete()
        messages.success(request, 'Registro de bitácora eliminado correctamente.')
        return redirect('proyecto_detail', proyecto_id=proyecto_id)
    return render(request, 'proyectos/bitacora_confirm_delete.html', {'bitacora': bitacora})

# Vista para filtrar datos
@login_required
def filtrar_datos(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        estado = request.GET.get('estado')
        fecha_inicio = request.GET.get('fecha_inicio')

        proyectos = Proyecto.objects.all()

        if query:
            proyectos = proyectos.filter(nombre__icontains=query)
        if estado:
            proyectos = proyectos.filter(estado=estado)
        if fecha_inicio:
            proyectos = proyectos.filter(fecha_inicio__gte=fecha_inicio)

        proyectos_activos = proyectos.filter(estado='Activo').count()
        proyectos_finalizados = proyectos.filter(estado='Finalizado').count()

        tareas = Tarea.objects.filter(proyecto__in=proyectos)
        tareas_totales = tareas.count()
        tareas_completadas = tareas.filter(estado='Completada').count()
        tareas_pendientes = tareas_totales - tareas_completadas

        bitacoras = Bitacora.objects.filter(proyecto__in=proyectos)
        if bitacoras.exists():
            avance_promedio = round(sum([b.avance for b in bitacoras]) / bitacoras.count(), 2)
        else:
            avance_promedio = 0

        proyectos_html = render_to_string('proyectos/proyectos_list.html', {'proyectos': proyectos})

        data = {
            'proyectos_activos': proyectos_activos,
            'proyectos_finalizados': proyectos_finalizados,
            'tareas_completadas': tareas_completadas,
            'tareas_pendientes': tareas_pendientes,
            'avance_promedio': avance_promedio,
            'proyectos_html': proyectos_html,
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def proyectos_list(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos/proyectos_list.html', {'proyectos': proyectos})

@login_required
def dashboard(request):
    # Estadísticas generales
    proyectos = Proyecto.objects.all()
    tareas = Tarea.objects.all()
    bitacoras = Bitacora.objects.all()

    # Datos para las tarjetas de resumen
    total_proyectos = proyectos.count()
    proyectos_pendientes = proyectos.filter(estado='Pendiente').count()
    proyectos_activos = proyectos.filter(estado='Activo').count()
    proyectos_finalizados = proyectos.filter(estado='Finalizado').count()
    
    total_tareas = tareas.count()
    tareas_completadas = tareas.filter(estado='Completada').count()
    tareas_en_progreso = tareas.filter(estado='En Progreso').count()
    tareas_pendientes = tareas.filter(estado='Pendiente').count()

    if total_proyectos > 0:
        porcentaje_completado = round((proyectos_finalizados / total_proyectos) * 100)
    else:
        porcentaje_completado = 0

    # Datos para el gráfico de prioridades
    prioridades = ['Alta', 'Media', 'Baja']
    prioridades_data = [
        tareas.filter(prioridad=1).count(),
        tareas.filter(prioridad=2).count(),
        tareas.filter(prioridad=3).count()
    ]

    # Datos para el gráfico de progreso mensual
    ultimos_6_meses = []
    progreso_mensual = []
    fecha_actual = datetime.now()
    
    for i in range(5, -1, -1):
        fecha = fecha_actual - timedelta(days=i*30)
        mes = fecha.strftime('%B')
        ultimos_6_meses.append(mes)
        
        # Calcular progreso basado en tareas completadas y bitácoras
        tareas_mes = tareas.filter(
            proyecto__fecha_inicio__year=fecha.year,
            proyecto__fecha_inicio__month=fecha.month
        )
        if tareas_mes.exists():
            completadas = tareas_mes.filter(estado='Completada').count()
            progreso = round((completadas / tareas_mes.count()) * 100)
        else:
            progreso = 0
            
        # Ajustar con información de bitácoras si existe
        bitacoras_mes = bitacoras.filter(
            fecha__year=fecha.year,
            fecha__month=fecha.month
        )
        if bitacoras_mes.exists():
            promedio_bitacoras = round(sum(b.avance for b in bitacoras_mes) / bitacoras_mes.count())
            progreso = round((progreso + promedio_bitacoras) / 2)
            
        progreso_mensual.append(progreso)

    # Datos para el gráfico de asignaciones
    top_usuarios = User.objects.annotate(
        num_tareas=Count('tareas_asignadas')
    ).order_by('-num_tareas')[:5]

    # Preparar datos para los gráficos
    proyectos_data = {
        'labels': ['Pendientes', 'Activos', 'Finalizados'],
        'data': [proyectos_pendientes, proyectos_activos, proyectos_finalizados],
        'colors': ['#dc3545', '#ffc107', '#198754']  # rojo, amarillo, verde
    }

    prioridades_data = {
        'labels': prioridades,
        'data': prioridades_data,
        'colors': ['#dc3545', '#ffc107', '#198754']  # rojo, amarillo, verde
    }

    progreso_data = {
        'labels': ultimos_6_meses,
        'data': progreso_mensual
    }

    asignaciones_data = {
        'labels': [f"{u.first_name} {u.last_name}" if u.first_name else u.username for u in top_usuarios],
        'data': [u.num_tareas for u in top_usuarios],
        'colors': ['#0d6efd', '#6610f2', '#6f42c1', '#d63384', '#dc3545']
    }

    context = {
        'total_proyectos': total_proyectos,
        'porcentaje_completado': porcentaje_completado,
        'tareas_completadas': tareas_completadas,
        'total_tareas': total_tareas,
        'tareas_en_progreso': tareas_en_progreso,
        'tareas_pendientes': tareas_pendientes,
        
        # Convertir los datos a JSON para los gráficos
        'proyectos': json.dumps(proyectos_data),
        'prioridades': json.dumps(prioridades_data),
        'progreso': json.dumps(progreso_data),
        'asignaciones': json.dumps(asignaciones_data)
    }

    return render(request, 'proyectos/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            
            profile = user.profile
            
            # Si se envía una nueva imagen
            if 'image' in request.FILES:
                # Eliminar la imagen anterior si no es la predeterminada
                if profile.image and profile.image.name != 'perfiles/default-avatar.png':
                    profile.image.delete(save=False)
                profile.image = request.FILES['image']
                profile.save()
            
            # Si se solicita eliminar la foto
            if 'delete_image' in request.POST:
                if profile.image and profile.image.name != 'perfiles/default-avatar.png':
                    profile.image.delete(save=False)
                profile.image = 'perfiles/default-avatar.png'
                profile.save()
            
            user.save()
            messages.success(request, 'Perfil actualizado correctamente')
        except Exception as e:
            messages.error(request, f'Error al actualizar el perfil: {str(e)}')
        return redirect('profile')
    
    try:
        # Asegurarse de que el perfil existe
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Si no existe, créalo
        profile = Profile.objects.create(user=request.user)
    
    return render(request, 'proyectos/profile.html')