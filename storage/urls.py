from django.contrib import admin
from django.urls import path, include
from storage import views

urlpatterns = [
    path('locations', views.Locations.as_view()),
    path('currencies', views.Currencies.as_view()),
    path('languages', views.Languages.as_view()),
    path('timezones', views.Timezones.as_view()),
]
