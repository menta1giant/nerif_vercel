from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Match, Team, PredictedMap, Capper, Endorsement

class MatchesTests(APITestCase):
    def setUp(self):
        self.team1 = Team.objects.create(team_id=1, name='Team 1')
        self.team2 = Team.objects.create(team_id=2, name='Team 2')
        self.match1 = Match.objects.create(match_id=1, team_favorite=self.team1, team_opponent=self.team2)
        self.match2 = Match.objects.create(match_id=2, team_favorite=self.team1, team_opponent=self.team2)

    def test_get_matches(self):
        url = reverse('matches')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_match_valid_data(self):
        url = reverse('matches')
        data = {'match_id': 3, 'team_favorite': 1, 'team_opponent': 2}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_match_invalid_data(self):
        url = reverse('matches')
        data = {'match_id': 3, 'team_favorite': 1, 'team_opponent': 3}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)

class MatchesOddsTests(APITestCase):
    def test_get_matches_odds(self):
        url = reverse('matches_odds')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PredictedMapsTests(APITestCase):
    def setUp(self):
        self.team1 = Team.objects.create(team_id=1, name='Team 1')
        self.team2 = Team.objects.create(team_id=2, name='Team 2')
        self.match1 = Match.objects.create(match_id=1, team_favorite=self.team1, team_opponent=self.team2)
        self.predicted_map1 = PredictedMap.objects.create(match=self.match1, map_order=1)
        self.predicted_map2 = PredictedMap.objects.create(match=self.match1, map_order=2)

    def test_get_predicted_maps(self):
        url = reverse('predicted_maps')
        data = {'date': '2023-07-28', 'offset': 0, 'limit': 10}
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_predicted_map_valid_data(self):
        url = reverse('predicted_maps')
        data = {'match': self.match1.pk, 'map_order': 3, 'match_date': '2020-01-01', 'odds_change': 0, 'team_favorite': 1, 'team_opponent': 2, 'team_favorite_name': 'Team1', 'team_opponent_name': 'Team2'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 200)

    def test_post_predicted_map_invalid_data(self):
        url = reverse('predicted_maps')
        data = {}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)

class PredictedMapStatsTests(APITestCase):
    def setUp(self):
        self.team1 = Team.objects.create(team_id=1, name='Team 1')
        self.team2 = Team.objects.create(team_id=2, name='Team 2')
        self.match1 = Match.objects.create(match_id=1, team_favorite=self.team1, team_opponent=self.team2)
        self.predicted_map1 = PredictedMap.objects.create(match=self.match1, map_order=1)

    def test_get_predicted_map_stats(self):
        url = reverse('predicted_map_stats', args=[self.predicted_map1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RulesetsTests(APITestCase):
    def test_get_rulesets(self):
        url = reverse('rulesets')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_ruleset_valid_data(self):
        url = reverse('rulesets')
        data = {'minimum': 0.0, 'maximum': 200.0, 'threshold': 130.0, 'is_favorite': True, 'pref': '010_01000_0_0'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_ruleset_invalid_data(self):
        url = reverse('rulesets')
        data = {'is_favorite': 'abc'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)

class CappersViewTests(APITestCase):
    def setUp(self):
        self.capper1 = Capper.objects.create(name='Capper 1')
        self.capper2 = Capper.objects.create(name='Capper 2')

    def test_get_cappers(self):
        url = reverse('cappers')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class EndorsementsViewTests(APITestCase):
    def setUp(self):
        self.capper1 = Capper.objects.create(name='Capper 1')
        self.capper2 = Capper.objects.create(name='Capper 2')
        self.match1 = Match.objects.create(match_id=1)
        self.predicted_map1 = PredictedMap.objects.create(match=self.match1, map_order=1)
        self.endorsement1 = Endorsement.objects.create(author=self.capper1, related_map=self.predicted_map1, content='Endorsement 1')
        self.endorsement2 = Endorsement.objects.create(author=self.capper2, related_map=self.predicted_map1, content='Endorsement 2')

    def test_get_endorsements(self):
        url = reverse('endorsements')
        data = {'cappers': '1,2'}
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)