from rest_framework import routers,serializers,viewsets
from .models import Profile, Subscription
from django.utils import timezone
from storage.lists import PLAN_CHOICES, PLAN_PERIOD_CHOICES

class ProfileSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Profile
        fields = ['profile_photo']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['date_started', 'plan']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        today = timezone.localdate()

        representation['time_left'] = (today - instance.date_started).days + PLAN_PERIOD_CHOICES[instance.period][0]
        representation['plan'] = PLAN_CHOICES[representation['plan']][1]

        return representation