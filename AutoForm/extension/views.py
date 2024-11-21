from django.http import JsonResponse
import json
from django.shortcuts import redirect, render
from .models import Informacion_personal,Telefono,Email,Perfil_laboral,Hoja_vida,Cargo
from django.contrib.auth.decorators import login_required
from .utils.form_embeddings import similarity_search
from django.views.decorators.csrf import csrf_exempt
from .forms import pdf_upload
from PyPDF2 import PdfReader
import requests
import os


def retornar_json(request):
    if request.method == 'GET':
        json = {'mensaje':'este es un mensaje enviado desde el backend'}
        return JsonResponse(json)

@csrf_exempt
def recibir_forms(request):
    if (request.method == 'POST'):
        user = request.user
        informacion_personal = Informacion_personal.objects.filter(usuario_id=user).first()
    
        print(request.body)
        json_form = json.loads(request.body)
        form_info = json_form["forms"]
        print(form_info)
        for key, value in form_info.items():
            if key != 'csrfmiddlewaretoken':
                print(key, value)
                processed_field = similarity_search(key)
                
                print(processed_field)

                if key == 'phone' or processed_field == 'telefono':
                    telefono = Telefono.objects.filter(id_informacion_personal=informacion_personal).first() # Cambiar a escoger telefono
                    form_info[key] = '+' + telefono.extension + ' ' + telefono.numero

                elif key == 'name' or processed_field == 'nombre' or processed_field == 'name':
                    form_info[key] = informacion_personal.nombre
                elif key == 'last_name' or processed_field == 'apellidos' or processed_field == 'last_name':
                    form_info[key] = informacion_personal.apellidos
                elif key == 'gender' or processed_field == 'genero' or processed_field == 'gender':    
                    form_info[key] = informacion_personal.genero
                elif key == 'email' or processed_field == 'email':
                    email = Email.objects.filter(id_informacion_personal=informacion_personal).first()
                    form_info[key] = str(email.email)
                elif key == 'id' or processed_field == 'identificacion' or processed_field == 'id':
                    form_info[key] = informacion_personal.identificacion
                elif key == 'address' or processed_field == 'direccion' or processed_field == 'address':
                    form_info[key] = informacion_personal.residencia
                elif key == 'birthdate' or processed_field == 'fecha_nacimiento' or processed_field == 'birthdate':
                    form_info[key] = str(informacion_personal.fecha_nacimiento)
                else:
                    form_info[key] = 'No se encontró información'

        response = {'status':'success', "forms":form_info}
        print(response)
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
        hoja_de_vida = request.FILES.get('hoja_de_vida')  # Capturar el archivo subido
        nuevo_perfil_laboral = Perfil_laboral(nombre_perfil=nombre_perfil,expectativa_salario=expectativa_salario,id_usuario=request.user,hoja_de_vida=hoja_de_vida)
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




@login_required
def eliminar_perfil_laboral(request,perfil_id):
    perfil_laboral = Perfil_laboral.objects.get(pk = perfil_id)
    perfil_laboral.delete()
    return redirect('informacion_usuario')





def recomendar_mejoras(request):
    suggestions = None

    if request.method == 'POST':
        form = pdf_upload(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']

            # Leer el token de Hugging Face desde el archivo JSON
            with open(os.path.join(os.path.dirname(__file__), 'utils', 'hf_token.json')) as f:
                hf_token = json.load(f)['hf_token_LLM']

            # Extraer texto del PDF
            try:
                pdf_reader = PdfReader(pdf_file)
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"

                # Verificar que se haya extraído texto
                if not text_content.strip():
                    return JsonResponse({"error": "No se pudo extraer texto del PDF."}, status=400)
            except Exception as e:
                return JsonResponse({"error": f"Error al leer el PDF: {str(e)}"}, status=500)

            
            api_url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1" 
            headers = {
                'Authorization': f'Bearer {hf_token}',
                'Content-Type': 'application/json'
            }
            payload = {
                "inputs": f"<s> [INST] Revise el siguiente currículum y proporcione sugerencias de mejora, el objetivo es lograr un perfil laboral atractivo con el que contraten facilente:   Este es el perfil laboral ({text_content}), de sus recomendaciones[/INST]",
                "parameters": {
                    "return_full_text": False  
                }
            }

            # Enviar solicitud a Hugging Face
            response = requests.post(api_url, headers=headers, json=payload)

            if response.status_code != 200:
                return JsonResponse({"error": "Error en la solicitud a la API de Hugging Face.", "details": response.text}, status=500)

            # Obtener la respuesta de Hugging Face
            response_data = response.json()
            
            print(response_data)
            # Procesar y limpiar la respuesta
            if isinstance(response_data, list) and "generated_text" in response_data[0]:
                # Extraer texto, eliminar caracteres innecesarios, y dividirlo en sugerencias
                raw_text = response_data[0]["generated_text"]
                cleaned_text = raw_text.replace("\n", " ").replace("Sugerencias:", "").strip()
                suggestions = [s.strip() for s in cleaned_text.split("1.") if s]  
            else:
                suggestions = []
    else:
        form = pdf_upload()

    return render(request, 'sugerencias_cv.html', {'form': form, 'suggestions': suggestions})