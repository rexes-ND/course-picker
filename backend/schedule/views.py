from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Hello, world!")

def arg(request):
    return HttpResponse("Hello from the arg")