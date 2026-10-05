from django.http import HttpResponse
from django.shortcuts import render

from meetings.models import Meeting

def welcome(request):
    return render(request, "website/welcome.html", {"meetings": Meeting.objects.all()})#dictionary is passed to the template

def about(request):
    return HttpResponse("Hello my name is erika")