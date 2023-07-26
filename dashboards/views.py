from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .utils import generate_data_and_labels_for_profits_chart, generate_data_and_labels_for_odds_intervals_chart, generate_stats_table_data
from .tables import STATS_TABLE_COLUMNS

class ProfitsView(APIView):
    def get(self, request):
        data, labels = generate_data_and_labels_for_profits_chart()

        return JsonResponse({
            'data': data,
            'labels': labels,
        })
    
class OddsIntervalsView(APIView):
    def get(self, request):
        data, labels = generate_data_and_labels_for_odds_intervals_chart()

        return JsonResponse({
            'data': data,
            'labels': labels,
        })
    
class StatsView(APIView):
    def get(self, request):
        data = generate_stats_table_data()
        
        return JsonResponse({
            'data': data,
            'columns': STATS_TABLE_COLUMNS,
        })
    
class UpsetsView(APIView):
    def get(self, request):
        return Response(status=200)
    