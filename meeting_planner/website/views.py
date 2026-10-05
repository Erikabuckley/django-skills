from django.shortcuts import render
from django.http import HttpResponse

def welcome(request):
    return render(request, "website/welcome.html")

def about(request):
    return HttpResponse("Hello my name is erika")