from rest_framework import routers,serializers,viewsets
from .models import Match, UpcomingCoeff, Team, RuleSet, PredictedMap, Endorsement, Capper

class RulesetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleSet
        fields = '__all__'

class CapperOptionSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='name')

    class Meta:
        model = Capper
        fields = ('id', 'label')

class CapperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capper
        fields = '__all__'

class EndorsementSerializer(serializers.ModelSerializer):
    author = CapperSerializer(read_only=True)

    class Meta:
        model = Endorsement
        fields = '__all__'

class ScoresSideSerializer(serializers.Serializer):
    score = serializers.FloatField()
    ruleset = RulesetSerializer()

class ScoreSerializer(serializers.Serializer):
    favorite = ScoresSideSerializer()
    opponent = ScoresSideSerializer()

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    match_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)

    class Meta:
        model = Match
        fields = ['match_id', 'match_date', 'team_favorite', 'team_opponent', 'odds_change']
    
    def to_representation(self, instance):
        self.fields['team_favorite'] = TeamSerializer(read_only=True)
        self.fields['team_opponent'] = TeamSerializer(read_only=True)
        return super().to_representation(instance)

class PredictedMapStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictedMap
        fields = [
            'bookmakers_spread',
            'prematch',
            'comfortability',
            'certainty_change',
            'previous_map_offset',
            'recent_performance',
            'percentage_of_played',
            'banned_when_could',
            'opponent_score',
            'previous_map_score',
            'map_score',
            'map_count',
            'map_winrate',
            'map_streak',
            'streak',
            'picked_to_played',
        ]

class PredictedMapPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictedMap
        fields = '__all__'
    
class PredictedMapGetSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)

    class Meta:
        model = PredictedMap
        fields = ['match', 'map_order', 'date_predicted', 'pick_category']
    
    def to_representation(self, instance):
        self.fields['ruleset_favorite'] = RulesetSerializer()
        self.fields['ruleset_opponent'] = RulesetSerializer()
        representation = super().to_representation(instance)

        representation['id'] = instance.pk

        representation['match']['team_favorite']['map_score'] = instance.map_score_favorite
        representation['match']['team_opponent']['map_score'] = instance.map_score_opponent
        representation['match']['team_favorite']['odds'] = instance.odds_favorite
        representation['match']['team_opponent']['odds'] = instance.odds_opponent

        endorsements = Endorsement.objects.all().filter(related_map = instance.pk)

        representation['endorsements'] = {
            'favorite': endorsements.filter(is_favorite = True).count(),
            'opponent': endorsements.filter(is_favorite = False).count(),
        }

        representation['scores'] = {
            'favorite': {
                'score': instance.score_favorite,
                'ruleset': representation['ruleset_favorite'],
                'is_predicted': instance.score_favorite >= representation['ruleset_favorite']['threshold'] if representation['ruleset_favorite'] else False,
            },
            'opponent': {
                'score': instance.score_opponent,
                'ruleset': representation['ruleset_opponent'],
                'is_predicted': instance.score_opponent <= representation['ruleset_opponent']['threshold'] if representation['ruleset_opponent'] else False,
            },
        }

        del representation['ruleset_favorite']
        del representation['ruleset_opponent']
        return representation
    
class PredictedMapsMetaSerializer(serializers.Serializer):
    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        user_serializer = PredictedMapGetSerializer(instance, many=True)
        return user_serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {'data': representation['data'], **self.context}
    
class UpcomingCoeffSerializer(serializers.ModelSerializer):
    match_id = serializers.IntegerField(source='match.match_id', read_only=True)
    odds = serializers.FloatField()
    date_added = serializers.DateTimeField(format="%H:%M")

    class Meta:
        model = UpcomingCoeff
        fields=('match_id', 'odds', 'date_added')