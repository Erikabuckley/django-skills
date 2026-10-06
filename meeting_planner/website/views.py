from django.http import HttpResponse
from django.shortcuts import render

from meetings.models import Meeting

def welcome(request):
    if request.user.is_authenticated:
        context =  {"meetings": Meeting.objects.all()}
    else:
        context = {}
    return render(request, "website/welcome.html",context)#dictionary is passed to the template

def about(request):
    return HttpResponse("Hello my name is erika")