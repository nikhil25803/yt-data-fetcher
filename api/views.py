from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
async def index(request):

    return JsonResponse(data={"message": "API is up and running!"})
