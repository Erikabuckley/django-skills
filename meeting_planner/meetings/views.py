from django import forms
from django.forms import modelform_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.shortcuts import render, get_object_or_404, redirect

from datetime import datetime, timedelta

from meetings.models import Meeting, Room

# creates a template for the meeting form
MeetingForm = modelform_factory(
    Meeting,
    exclude=[],
    widgets={
        "date": forms.DateInput(attrs={"type": "date"}),
    },
)


# function to check if the meetin times overlap with the new times
def check_overlap(form, new):
    meeting = form.save(commit=False)

    meetings = Meeting.objects.filter(date=meeting.date, room=meeting.room)

    new_start = datetime.combine(meeting.date, meeting.start_time)
    new_end = new_start + timedelta(hours=meeting.duration)

    for existing in meetings:
        existing_start = datetime.combine(existing.date, existing.start_time)
        existing_end = existing_start + timedelta(hours=existing.duration)

        if new_start < existing_end and new_end > existing_start:
            form.add_error(None, "This room is already booked during that time.")
            return None

    meeting.save()
    form.save_m2m()
    if new:
        return redirect("welcome")
    else:
        return redirect("detail", id)


# view to send sign up data to the backend
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            print("Account created sucesfully")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


# view to get the the requested meeting
@login_required
def detail(request, id):
    meeting = get_object_or_404(
        Meeting, pk=id
    )  # returns 404 if not found for or given class with id
    return render(request, "meetings/detail.html", {"meeting": meeting})


# gets the list of rooms in the building
@login_required
def rooms_list(request):
    return render(request, "meetings/rooms.html", {"rooms": Room.objects.all()})


# adds a new meeting and stores it
@login_required
def new(request):
    if request.method == "POST":
        form = MeetingForm(request.POST)
        # checks if fields are valid
        if form.is_valid():
            response = check_overlap(form, True)
            if response is not None:
                return response
    else:
        form = MeetingForm()
    # if form was not valid its called again
    return render(request, "meetings/new.html", {"form": form})


# updates meeting values
@login_required
def edit(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    if request.method == "POST":
        form = MeetingForm(request.POST, instance=meeting)
        # checks if fields are valid
        if form.is_valid():
            response = check_overlap(form, False)
            if response is not None:
                return response

    else:
        form = MeetingForm(instance=meeting)
    # if form was not valid its called again
    return render(request, "meetings/edit.html", {"form": form})


# deltes the meeting
@login_required
def delete(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    if request.method == "POST":
        meeting.delete()
        return redirect("welcome")
    else:
        return render(request, "meetings/confirm_delete.html", {"meeting": meeting})


# itterates over meetings to find if room is occupied or not
@require_GET
def get_occupied(request):
    name = request.GET.get("name")
    meetings = Meeting.objects.filter(room__name=name, date=timezone.localdate())

    now = timezone.localtime()

    for meeting in meetings:
        start = datetime.combine(meeting.date, meeting.start_time)
        end = start + timedelta(hours=meeting.duration)

        if start <= now.replace(tzinfo=None) < end:
            return JsonResponse({"occupied": True})

    return JsonResponse({"occupied": False})


# gets the dates for the persons meetings that month
@require_GET
def get_dates(request):
    current_month = request.GET.get("month")
    current_year = request.GET.get("year")
    meetings = Meeting.objects.filter(
        date__month=current_month,
        date__year=current_year,
        participants__id=request.user.id,
    )

    dates = sorted(set(meeting.date.day for meeting in meetings))

    return JsonResponse({"dates": dates})
