from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    #return HttpResponse('<html><title>FoodSugar</title></html>')
    return render(request, 'index.html')
