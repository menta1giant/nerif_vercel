from django.contrib import admin
from django.urls import path, include
from dashboards import views

urlpatterns = [
    path('profits', views.ProfitsView.as_view()),
    path('odds-intervals', views.OddsIntervalsView.as_view()),
    path('stats', views.StatsView.as_view()),
    path('upsets', views.UpsetsView.as_view()),
]
