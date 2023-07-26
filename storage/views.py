from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from .utils import preformatResource
from .lists import LOCATION_CHOICES, CURRENCY_CHOICES, LANGUAGE_CHOICES, TIMEZONE_CHOICES

class Locations(APIView):
    def get(self, request):
        return JsonResponse(preformatResource(LOCATION_CHOICES), safe=False)
    
class Currencies(APIView):
    def get(self, request):
        return JsonResponse(preformatResource(CURRENCY_CHOICES), safe=False)
    
class Languages(APIView):
    def get(self, request):
        return JsonResponse(preformatResource(LANGUAGE_CHOICES), safe=False)
    
class Timezones(APIView):
    def get(self, request):
        return JsonResponse(preformatResource(TIMEZONE_CHOICES), safe=False)