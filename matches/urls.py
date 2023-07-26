from django.contrib import admin
from django.urls import path, include
from matches import views

urlpatterns = [
    path('', views.Matches.as_view()),
    path('cappers/', views.CappersView.as_view()),
    path('endorsements/', views.EndorsementsView.as_view()),
    path('predictions/maps', views.PredictedMaps.as_view()),
    path('predictions/stats/<int:id>', views.PredictedMapStats.as_view()),
    path('rulesets', views.Rulesets.as_view()),
    path('predictions/odds', views.MatchesOdds.as_view()),
]
