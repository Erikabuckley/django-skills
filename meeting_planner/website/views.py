import requests
import os
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache

from meetings.models import Meeting

logger = logging.getLogger(__name__)


# loads welcome page and filters data dependant on authentication leel
def welcome(request):
    if request.user.is_authenticated:
        context = {
            "meetings": Meeting.objects.filter(
                participants__id=request.user.id, date__gt=timezone.now()
            ),
            "pastmeetings": Meeting.objects.filter(
                participants__id=request.user.id, date__lt=timezone.now()
            ).order_by("-date"),
        }

    else:
        context = {}
    return render(
        request, "website/welcome.html", context
    )  # dictionary is passed to the template


# gets the currrent weather at teh requests lat and long
@require_GET
@never_cache
def get_weather_data(request):
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

        if not response.ok:
            logger.error(
                "Weather API failed: status=%s body=%s",
                response.status_code,
                response.text[:500],
            )

        response.raise_for_status()
        return JsonResponse(response.json())

    except requests.RequestException:
        logger.exception("Weather API request failed")
        return JsonResponse(
            {"error": "Could not retrieve weather data"},
            status=502,
        )


# gets the riddle for
@require_GET
def get_riddle(request):
    api_key = os.getenv("RIDDLE_KEY")

    if not api_key:
        return JsonResponse(
            {"error": "API key is not configured"},
            status=500,
        )

    try:
        response = requests.get(
            "https://api.apileague.com/retrieve-random-riddle",
            headers={
                "x-api-key": api_key,
            },
            timeout=10,
        )
        if not response.ok:
            logger.error(
                "Riddle API failed: status=%s body=%s",
                response.status_code,
                response.text[:500],
            )
        response.raise_for_status()

        return JsonResponse(response.json(), safe=False)

    except requests.RequestException:
        return JsonResponse(
            {"error": "Could not retrieve riddle"},
            status=502,
        )
