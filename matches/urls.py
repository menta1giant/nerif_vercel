from django.contrib import admin
from django.urls import path, include
from matches import views

urlpatterns = [
    path('', views.Matches.as_view(), name='matches'),
    path('cappers/', views.CappersView.as_view(), name='cappers'),
    path('endorsements/', views.EndorsementsView.as_view(), name='endorsements'),
    path('predictions/maps', views.PredictedMaps.as_view(), name='predicted_maps'),
    path('predictions/stats/<int:id>', views.PredictedMapStats.as_view(), name='predicted_map_stats'),
    path('rulesets', views.Rulesets.as_view(), name='rulesets'),
    path('predictions/odds', views.MatchesOdds.as_view(), name='matches_odds'),
]
