from django.db import models
from datetime import datetime 
from django.contrib.postgres.fields import ArrayField

def default_map_stat_normalized():
  return [0.5, 0.5]

class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Match(models.Model):
    match_id = models.IntegerField(primary_key=True)
    match_date = models.DateTimeField(default=datetime.now)
    team_favorite = models.ForeignKey(Team, default=1, on_delete=models.SET_DEFAULT, related_name="team_favorite")
    team_opponent = models.ForeignKey(Team, default=2, on_delete=models.SET_DEFAULT, related_name="team_opponent")
    odds_change = models.FloatField(default=0.0)
    
class RuleSet(models.Model):
    minimum = models.FloatField(default=0.0)
    maximum = models.FloatField(default=200.0)
    threshold = models.FloatField(default=130.0)
    is_favorite = models.BooleanField(default=True)
    pref = models.CharField(max_length=20, default='010_01000_0_0')

    def __str__(self):
        return str(self.pk)

class Capper(models.Model):
    name = models.CharField(max_length=100)
    link = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class PredictedMap(models.Model):
    match = models.ForeignKey(Match, default=0, on_delete=models.SET_DEFAULT)
    map_order = models.IntegerField(default=1)
    date_predicted = models.DateTimeField(auto_now_add=True)
    
    odds_favorite = models.FloatField(default=1.5)
    odds_opponent = models.FloatField(default=3.25)
    score_favorite = models.FloatField(default=None, null=True)
    score_opponent = models.FloatField(default=None, null=True)
    ruleset_favorite = models.ForeignKey(RuleSet, default=None, on_delete=models.SET_DEFAULT, related_name="ruleset_favorite", null=True)
    ruleset_opponent = models.ForeignKey(RuleSet, default=None, on_delete=models.SET_DEFAULT, related_name="ruleset_opponent", null=True)

    pick_category = models.IntegerField(default=0)

    map_score_favorite = models.IntegerField(default=8)
    map_score_opponent = models.IntegerField(default=13)

    #stats
    bookmakers_spread = models.FloatField(default=0.5)
    prematch = models.FloatField(default=0.5)
    comfortability = models.FloatField(default=0.5)
    certainty_change = models.FloatField(default=0.5)
    previous_map_offset = ArrayField(models.FloatField(), default=default_map_stat_normalized, size=2)
    recent_performance = ArrayField(models.FloatField(), default=default_map_stat_normalized, size=2)
    percentage_of_played = ArrayField(models.FloatField(), default=default_map_stat_normalized, size=2)
    banned_when_could = ArrayField(models.FloatField(), default=default_map_stat_normalized, size=2)
    opponent_score = ArrayField(models.FloatField(), default=default_map_stat_normalized, size=2)
    previous_map_score = ArrayField(models.FloatField(), default=default_map_stat_normalized, size=2)
    map_score = ArrayField(models.FloatField(), default=default_map_stat_normalized, size=2)
    map_count = ArrayField(models.FloatField(), default=default_map_stat_normalized, size=2)
    map_winrate = ArrayField(models.FloatField(), default=default_map_stat_normalized, size=2)
    map_streak = ArrayField(models.FloatField(), default=default_map_stat_normalized, size=2)
    streak = ArrayField(models.FloatField(), default=default_map_stat_normalized, size=2)
    picked_to_played = ArrayField(models.FloatField(), default=default_map_stat_normalized, size=2)

    class Meta:
       unique_together = (("match", "map_order"),)

    def __str__(self):
        return str(self.pk)
    
class Endorsement(models.Model):
    related_map = models.ForeignKey(PredictedMap, default=0, on_delete=models.SET_DEFAULT, null=True)
    link = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Capper, default=0, on_delete=models.SET_DEFAULT)
    is_favorite = models.BooleanField(default=True)
    content = models.TextField()

    def __str__(self):
        return f'{self.author.name}: {self.content[:30]}'

class UpcomingCoeff(models.Model):
    match = models.ForeignKey(Match, default=0, on_delete=models.SET_DEFAULT)
    odds = models.FloatField(default=0.0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.match.match_id)