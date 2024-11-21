from django.urls import path,include
from . import views

urlpatterns = [
    path('retornar_json/', views.retornar_json,name = "retornar_json"),
    path('recibir_forms/', views.recibir_forms, name = "recibir_forms"),
    path('home/', views.home, name = "home"),
    path('validar_sesion/', views.validar_sesion, name = "validar_sesion"),
    
    path('llenado_informacion_usuario/', views.llenado_informacion_usuario, name = "llenado_informacion_usuario"),
    path('crear_perfil_laboral/', views.crear_perfil_laboral, name = "crear_perfil_laboral"),
    path('llenado_success/', views.llenado_success, name="llenado_success"),
    path('informacion_usuario/', views.informacion_usuario, name = "informacion_usuario"),

    path('eliminar_informacion_usuario/', views.eliminar_informacion_usuario, name = "eliminar_informacion_usuario"),
    path('recomendar_mejoras/', views.recomendar_mejoras, name='recomendar_mejoras'),
    path('eliminar_perfil_laboral/<int:perfil_id>/', views.eliminar_perfil_laboral, name='eliminar_perfil_laboral'),


]