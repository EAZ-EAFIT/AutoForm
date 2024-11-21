from django.db import models
from django.contrib.auth.models import User


class Informacion_personal(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=30)
    residencia = models.CharField(max_length=150)
    usuario_id = models.ForeignKey(User,on_delete=models.CASCADE)



class Telefono(models.Model):
    extension = models.CharField(max_length=10)
    numero = models.CharField(max_length=20)
    id_informacion_personal = models.ForeignKey(Informacion_personal,on_delete=models.CASCADE)




class Email(models.Model):
    email = models.EmailField(max_length=100)
    id_informacion_personal = models.ForeignKey(Informacion_personal,on_delete=models.CASCADE)




class Perfil_laboral(models.Model):
    nombre_perfil = models.CharField(max_length=40)
    expectativa_salario = models.FloatField()
    id_usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    hoja_de_vida = models.FileField(upload_to='hojas_de_vida/', blank=True, null=True)  # Campo para cargar el PDF




class Hoja_vida(models.Model):
    hoja_vida = models.FileField(upload_to='hojas_vida/')
    informacion_extraida = models.JSONField()
    id_perfil_laboral = models.ForeignKey(Perfil_laboral, on_delete=models.CASCADE)




class Cargo(models.Model):
    cargo = models.CharField(max_length=50)
    id_perfil_laboral = models.ForeignKey(Perfil_laboral,on_delete=models.CASCADE)