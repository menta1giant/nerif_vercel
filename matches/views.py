from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Match, PredictedMap, Team, UpcomingCoeff, RuleSet, Endorsement, Capper
from .serializers import MatchSerializer, UpcomingCoeffSerializer, PredictedMapPostSerializer, PredictedMapsMetaSerializer, RulesetSerializer, PredictedMapStatsSerializer, CapperOptionSerializer, EndorsementSerializer
from datetime import datetime
from django.db.models import F, Q
from .utils import generate_data_and_labels_for_upcoming_match_odds_chart
import time

class Matches(APIView):
    def get(self, request, format=None):
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        data = JSONParser().parse(request)

        serializer = MatchSerializer(data=data)

        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, 200)

        return Response(serializer.data, 400)
    
class MatchesOdds(APIView):
    def get(self, request, format=None):
        data, labels = generate_data_and_labels_for_upcoming_match_odds_chart()

        return JsonResponse({
            'data': data,
            'labels': labels,
        })

class PredictedMapStats(APIView):
    def get(self, request, *args, **kwargs):
        map_id = kwargs['id']

        map_instance = PredictedMap.objects.get(pk = map_id)

        serializer = PredictedMapStatsSerializer(map_instance)
        return Response(serializer.data)

class PredictedMaps(APIView):
    def get(self, request, format=None):
        data = request.query_params
        date = datetime.strptime(data.get('date'), "%Y-%m-%d")
        offset = int(data.get('offset'))
        limit = int(data.get('limit'))
        range = (offset, offset + limit)

        predicted_maps = PredictedMap.objects.all()

        predicted_maps = predicted_maps.filter(match__match_date__year=date.year, match__match_date__month=date.month, match__match_date__day=date.day)
        if (not('fav_pick') in data):
            predicted_maps = predicted_maps.exclude(Q(ruleset_favorite__pref__startswith='010') | Q(ruleset_opponent__pref__startswith='010'))

        if (not('opp_pick') in data):
            predicted_maps = predicted_maps.exclude(Q(ruleset_favorite__pref__startswith='001') | Q(ruleset_opponent__pref__startswith='001'))

        if (not('fav_won_first') in data):
            predicted_maps = predicted_maps.exclude(Q(ruleset_favorite__pref__contains='01000') | Q(ruleset_opponent__pref__contains='01000'))

        if (not('opp_won_first') in data):
            predicted_maps = predicted_maps.exclude(Q(ruleset_favorite__pref__contains='00100') | Q(ruleset_opponent__pref__contains='00100'))

        if (not('map1') in data):
            predicted_maps = predicted_maps.exclude(map_order=1)

        if (not('map2') in data):
            predicted_maps = predicted_maps.exclude(map_order=2)

        if (not('map3') in data):
            predicted_maps = predicted_maps.exclude(map_order=3)

        if ('only_predicted' in data):
            predicted_maps = predicted_maps.filter(Q(score_favorite__gte = F('ruleset_favorite__threshold')) | Q(score_opponent__lte = F('ruleset_opponent__threshold')))

        if ('only_endorsed' in data):
            endorsements = Endorsement.objects.all()
            predicted_maps = predicted_maps.filter(pk__in=endorsements.values_list('pk', flat=True))

        predicted_maps_count = predicted_maps.count()
        predicted_maps_limited = predicted_maps[range[0] : range[1]]

        is_enough = predicted_maps_count <= range[1]
        serializer = PredictedMapsMetaSerializer(predicted_maps_limited, context={ 'is_enough': is_enough, 'total': predicted_maps_count })

        return Response(serializer.data)
    
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        try:
          pmap = PredictedMap.objects.get(match__match_id = data['match'], map_order = data['map_order'])
          serializer = PredictedMapPostSerializer(pmap, data=data)
        except PredictedMap.DoesNotExist:
            try:
                team_favorite, created_favorite = Team.objects.get_or_create(team_id=data['team_favorite'], defaults={ 'name': data['team_favorite_name'] })
                team_opponent, created_opponent = Team.objects.get_or_create(team_id=data['team_opponent'], defaults={ 'name': data['team_opponent_name'] })
                match, created_match = Match.objects.get_or_create(match_id=data['match'], defaults={ 
                    'match_date': data['match_date'], 
                    'odds_change': data['odds_change'], 
                    'team_favorite': team_favorite, 
                    'team_opponent': team_opponent 
                })

                serializer = PredictedMapPostSerializer(data=data)
            except:
                return Response(status=400)
        except: return Response(status=400)
        
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, 200)
        
        return Response(serializer.data, 400)
    
class Rulesets(APIView):
    def get(self, request, format=None):
        rulesets = RuleSet.objects.all()
        serializer = RulesetSerializer(rulesets, many=True)
        return Response(serializer.data)
     
    def post(self, request, format=None):
        data = JSONParser().parse(request)

        serializer = RulesetSerializer(data=data)
        
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, 200)
        
        return Response(serializer.data, 400)
    
class CappersView(APIView):
    def get(self, request):
        cappers = Capper.objects.all()

        serializer = CapperOptionSerializer(cappers, many=True)
        return Response(serializer.data)
    
class EndorsementsView(APIView):
    def get(self, request):
        cappers = request.query_params.get('cappers')
        endorsements = Endorsement.objects.all()
        if (cappers):
            cappers = cappers.split(',')

            endorsements = endorsements.filter(author__pk__in=cappers)

        serializer = EndorsementSerializer(endorsements, many=True)
        return Response(serializer.data)