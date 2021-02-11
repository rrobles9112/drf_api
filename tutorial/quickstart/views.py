from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .services import get_weather
from datetime import datetime, date


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def degrees_to_cardinal(d):
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(d / (360. / len(dirs)))
    return dirs[ix % len(dirs)]


def get_time(dt):
    b = date.fromtimestamp(dt)
    time_b = b.strftime('%a, %d %b %Y %H:%M:%S')
    return time_b


class WeatherView(APIView):

    """
        Request external weather api and output formatted response.
    """
    #@method_decorator(cache_page(60*60*2))
    def get(self, request, country, city):
        data = dict(get_weather(country, city))

        content = {
            "location_name": f"{city}, {country.upper()}",
            "temperature": data['main']['temp'],
            "wind": f"{data['wind']['speed']} m/s, {degrees_to_cardinal(data['wind']['deg'])}",
            "cloudiness": data['weather'][0]['description'],
            "pressure": f"{data['main']['pressure']} hpa",
            "humidity": f"{data['main']['humidity']}%",
            "sunrise": get_time(data['sys']['sunrise']),
            "sunset": get_time(data['sys']['sunset']),
            "geo_coordinates": [data['coord']['lon'], data['coord']['lat']],
            "requested_time": data['dt']

        }

        return Response(content)
