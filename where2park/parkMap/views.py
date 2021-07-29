from django.shortcuts import render
from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at parkMap index.")

def index(request):
    context = {'hi'}
    return render(request, 'parkMap/index.html')

def detail(request, meter_id):
    return HttpResponse("You're looking at meter %s." % meter_id)