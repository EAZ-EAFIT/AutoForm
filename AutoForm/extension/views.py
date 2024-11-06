from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect, render
from .models import Informacion_personal,Telefono,Email,Perfil_laboral,Hoja_vida,Cargo
from django.contrib.auth.decorators import login_required


def retornar_json(request):
    if request.method == 'GET':
        json = {'mensaje':'este es un mensaje enviado desde el backend'}
        return JsonResponse(json)

@csrf_exempt
def recibir_forms(request):
    if (request.method == 'POST'):
        print(request.body)
        json_form = json.loads(request.body)
        form_info = json_form["forms"]
        for key, value in form_info.items():
            if key != 'csrfmiddlewaretoken':
                form_info[key] = "5890"


        response = {'status':'success', "forms":form_info}
        return JsonResponse(response)
    else:
        return {'status':'failure'}



"""Vista home"""
def home(request):
    return render(request,'home.html')




"""Vista que recibe cookies, verifica si usuario se encuentra autenticado y le manda dicha info al front"""
def validar_sesion(request):
    if request.user.is_authenticated:
        return JsonResponse({'autenticado':True})
    else:
        return JsonResponse({'autenticado':False})





"""Vista que permite llenado de información usuarios"""
@login_required
def llenado_informacion_usuario(request):

    context = {}
    
    if Informacion_personal.objects.filter(usuario_id=request.user).exists(): #Si ya tiene información personal:
        context['ya_ingreso_info_personal'] = True
    
    if request.method == "POST":
        #Se obtiene información de formulario
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        identificacion = request.POST.get('identificacion')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        genero = request.POST.get('genero')
        residencia = request.POST.get('residencia')
        extension = request.POST.get('extension')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')

        informacion_personal = Informacion_personal(nombre=nombre,apellidos=apellidos,identificacion=identificacion,fecha_nacimiento=fecha_nacimiento,genero=genero,residencia=residencia,usuario_id=request.user)
        nuevo_telefono = Telefono(extension=extension,numero=telefono,id_informacion_personal=informacion_personal)
        nuevo_email = Email(email=email,id_informacion_personal=informacion_personal)
        informacion_personal.save()
        nuevo_telefono.save()
        nuevo_email.save()
        return redirect('llenado_success')
    

    elif request.method == "GET":
        return render(request,"llenado_informacion_usuario.html",context=context)





"""Vista para crear un perfil laboral"""
@login_required
def crear_perfil_laboral(request):
    if request.method == "POST":
        nombre_perfil = request.POST.get('nombre_perfil')
        expectativa_salario = request.POST.get('expectativa_salario')
        nuevo_perfil_laboral = Perfil_laboral(nombre_perfil=nombre_perfil,expectativa_salario=expectativa_salario,id_usuario=request.user)
        nuevo_perfil_laboral.save()
        return redirect('informacion_usuario')
    

    elif request.method == "GET":
        return render(request,"crear_perfil_laboral.html")




@login_required
def llenado_success(request):
    return render(request,"llenado_success.html")



@login_required
def informacion_usuario(request):
    context = {}
    perfiles_laborales = Perfil_laboral.objects.filter(id_usuario=request.user)
    context['perfiles_laborales'] = perfiles_laborales
    try:
        informacion_personal = Informacion_personal.objects.get(usuario_id = request.user)
        telefonos = Telefono.objects.filter(id_informacion_personal=informacion_personal)
        emails = Email.objects.filter(id_informacion_personal=informacion_personal)
        context['emails'] = emails
        context['telefonos'] = telefonos
        context['informacion_personal'] = informacion_personal
    except Informacion_personal.DoesNotExist:
        context['informacion_personal'] = None

    
    return render(request,'informacion_usuario.html',context = context)






@login_required
def eliminar_informacion_usuario(request):

    informacion_usuario = Informacion_personal.objects.get(usuario_id = request.user)
    informacion_usuario.delete()

    return redirect('informacion_usuario')