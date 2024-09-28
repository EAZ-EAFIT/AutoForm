from django.shortcuts import render
from django.http import JsonResponse

def retornar_json(request):

    if request.method == 'GET':
        json = {'mensaje':'este es un mensaje enviado desde el backend'}
        return JsonResponse(json)
