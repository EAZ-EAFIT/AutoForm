from django.urls import path,include
from . import views

urlpatterns = [
    path('retornar_json/', views.retornar_json,name = "retornar_json"),
    path('recibir_forms/', views.recibir_forms, name = "recibir_forms")
]
