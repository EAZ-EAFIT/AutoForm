from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect, render

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