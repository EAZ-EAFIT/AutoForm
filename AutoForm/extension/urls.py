from django.urls import path,include
from . import views

urlpatterns = [
    path('retornar_json/', views.retornar_json,name = "retornar_json"),
]
