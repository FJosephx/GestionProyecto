from django.urls import path
from proyectos import views

urlpatterns = [
    path('', views.home, name='home'),
]
