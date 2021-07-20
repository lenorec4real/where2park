from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at parkMap index.")


def detail(request, meter_id):
    return HttpResponse("You're looking at meter %s." % meter_id)