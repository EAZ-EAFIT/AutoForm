from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def retornar_json(request):
    if request.method == 'GET':
        json = {'mensaje':'este es un mensaje enviado desde el backend'}
        return JsonResponse(json)

@csrf_exempt
def recibir_forms(request):
    print("hola")
    if (request.method == 'POST'):
        print(request.body)
        json_form = json.loads(request.body)
        form_info = json_form["forms"]
        for key, value in form_info.items():
            if value != 'csrfmiddlewaretoken':
                form_info[key] = "hello"


        response = {'status':'success', "forms":form_info}
        return JsonResponse(response)
    else:
        return {'status':'failure'}
