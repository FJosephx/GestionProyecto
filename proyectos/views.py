from django.shortcuts import render, get_object_or_404, redirect
from .models import Proyecto, Tarea, Bitacora
from .forms import ProyectoForm, TareaForm, BitacoraForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    bitacoras = proyecto.bitacoras.all()
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
            bitacora = form.save(commit=False)
            bitacora.proyecto = proyecto
            bitacora.save()
            messages.success(request, 'Registro de bitácora agregado correctamente.')
            return redirect('proyecto_detail', proyecto_id=proyecto.id)
    else:
        form = BitacoraForm()
    return render(request, 'proyectos/bitacora_form.html', {'form': form, 'proyecto': proyecto})

# Editar bitácora
@login_required
def bitacora_update(request, bitacora_id):
    bitacora = get_object_or_404(Bitacora, id=bitacora_id)
    if request.method == 'POST':
        form = BitacoraForm(request.POST, instance=bitacora)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de bitácora actualizado correctamente.')
            return redirect('proyecto_detail', proyecto_id=bitacora.proyecto.id)
    else:
        form = BitacoraForm(instance=bitacora)
    return render(request, 'proyectos/bitacora_form.html', {'form': form, 'proyecto': bitacora.proyecto})

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
