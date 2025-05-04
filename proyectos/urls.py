from django.urls import path
from proyectos import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('proyectos/', views.proyectos_list, name='proyectos_list'),
    path('proyecto/<int:proyecto_id>/', views.proyecto_detail, name='proyecto_detail'),
    path('proyecto/crear/', views.proyecto_create, name='proyecto_create'),
    path('proyecto/<int:proyecto_id>/editar/', views.proyecto_update, name='proyecto_update'),
    path('proyecto/<int:proyecto_id>/eliminar/', views.proyecto_delete, name='proyecto_delete'),
    path('proyecto/<int:proyecto_id>/tarea/crear/', views.tarea_create, name='tarea_create'),
    path('proyecto/<int:proyecto_id>/bitacora/crear/', views.bitacora_create, name='bitacora_create'),
    path('tarea/<int:tarea_id>/editar/', views.tarea_update, name='tarea_update'),
    path('tarea/<int:tarea_id>/eliminar/', views.tarea_delete, name='tarea_delete'),
    path('bitacora/<int:bitacora_id>/editar/', views.bitacora_update, name='bitacora_update'),
    path('bitacora/<int:bitacora_id>/eliminar/', views.bitacora_delete, name='bitacora_delete'),
    path('api/filtrar/', views.filtrar_datos, name='filtrar_datos'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='proyectos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
