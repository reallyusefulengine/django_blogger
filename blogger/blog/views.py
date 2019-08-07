from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Home page should go here...</h1>")

def about(request):
    return HttpResponse("<h1>About page should go here...</h1>")
