import requests
from django.shortcuts import render

import os

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache

from meetings.models import Meeting

def welcome(request):
    if request.user.is_authenticated:
        context =  {"meetings": Meeting.objects.filter(participants__id=request.user.id)}# gets only for that user
    else:
        context = {}
    return render(request, "website/welcome.html",context)#dictionary is passed to the template


@require_GET
@never_cache
def get_meeting_data(request):
    api_key = os.getenv("EXTERNAL_API_KEY")
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    if not api_key:
        return JsonResponse(
            {"error": "API key is not configured"},
            status=500,
        )
    try:
        response = requests.get(
                    "https://api.openweathermap.org/data/2.5/weather",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": api_key,
                        "units": "metric",
                    },
                    timeout=10,
                    )
        response.raise_for_status()

        return JsonResponse(response.json(), safe=False)

    except requests.RequestException:
        return JsonResponse(
            {"error": "Could not retrieve meeting data"},
            status=502,
        )