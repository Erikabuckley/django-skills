from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from meetings.models import Meeting, Room

from datetime import datetime, timedelta


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})

@login_required
def detail(request, id):
    meeting = get_object_or_404(Meeting, pk=id)#returns 404 if not found for or given class with id
    return render(request, "meetings/detail.html",{"meeting": meeting})

@login_required
def rooms_list(request):
    return render(request, "meetings/rooms.html",{"rooms": Room.objects.all()})


MeetingForm = modelform_factory(Meeting, exclude=[],     widgets={
        'date': forms.DateInput(attrs={'type': 'date'}),
    })

def check_overlap(form, new):
    meeting = form.save(commit=False)

    meetings = Meeting.objects.filter(
        date=meeting.date,
        room=meeting.room
    )

    new_start = datetime.combine(
        meeting.date, meeting.start_time
    )
    new_end = new_start + timedelta(hours=meeting.duration)

    for existing in meetings:
        existing_start = datetime.combine(
            existing.date, existing.start_time
        )
        existing_end = existing_start + timedelta(
            hours=existing.duration
        )

        if new_start < existing_end and new_end > existing_start:
            form.add_error(
                None,
                "This room is already booked during that time."
            )
            return None

    meeting.save()
    if new:
        return redirect("welcome")
    else:
        return redirect("detail", id)

@login_required
def new(request):
    if request.method == "POST":
        form = MeetingForm(request.POST)
        #checks if fields are valid
        if form.is_valid():
            response = check_overlap(form, True)
            if response is not None:
                return response
    else:
        form = MeetingForm()
    #if form was not valid its called again
    return render(request, "meetings/new.html", {"form" : form})

@login_required
def edit(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    if request.method == "POST":
        form = MeetingForm(request.POST, instance=meeting)
        #checks if fields are valid
        if form.is_valid():
            response = check_overlap(form, False)
            if response is not None:
                return response

    else:
        form = MeetingForm(instance=meeting)
    #if form was not valid its called again
    return render(request, "meetings/edit.html", {"form" : form})

@login_required
def delete(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    if request.method == "POST":
        meeting.delete()
        return redirect("welcome")
    else:
        return render(request, "meetings/confirm_delete.html", {"meeting" : meeting})