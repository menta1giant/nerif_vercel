from django import forms
from .models import User, Profile, UserNotificationSettings, Subscription
from storage.lists import LOCATION_CHOICES, CURRENCY_CHOICES, LANGUAGE_CHOICES, TIMEZONE_CHOICES, PLAN_CHOICES, PLAN_PERIOD_CHOICES
from django.core.validators import FileExtensionValidator

forms.Field.default_error_messages = {
    'required': ("Please fill in this field"),
}

class SignupPaymentInfoForm(forms.ModelForm):
    currency = forms.ChoiceField(choices = CURRENCY_CHOICES)
    card_info = forms.CharField(max_length=25, required=True)

    class Meta:
        model = User
        fields = ['currency', 'card_info']

class SignupPlanSetupForm(forms.ModelForm):
    period = forms.ChoiceField(choices = PLAN_PERIOD_CHOICES)
    plan = forms.ChoiceField(choices = PLAN_CHOICES)

    class Meta:
        model = Subscription
        fields = ['period', 'plan']

class SignupPersonalInfoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    location = forms.ChoiceField(choices = LOCATION_CHOICES)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'location']

class PersonalInfoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=25, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']

class PaymentInfoForm(forms.ModelForm):
    location = forms.ChoiceField(choices = LOCATION_CHOICES)
    currency = forms.ChoiceField(choices = CURRENCY_CHOICES)
    card_info = forms.CharField(max_length=25, required=True)

    class Meta:
        model = User
        fields = ['location', 'currency', 'card_info']

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)

class LocalizationInfoForm(forms.ModelForm):
    language = forms.ChoiceField(choices = LANGUAGE_CHOICES)
    timezone = forms.ChoiceField(choices = TIMEZONE_CHOICES)

    class Meta:
        model = User
        fields = ['language', 'timezone']

class NotificationSettingsForm(forms.ModelForm):
    new_predictions = forms.BooleanField(required=False)
    cappers_predictions = forms.BooleanField(required=False)
    dashboard_digests = forms.BooleanField(required=False)
    special_offers = forms.BooleanField(required=False)
    community_mentions = forms.BooleanField(required=False)

    class Meta:
        model = UserNotificationSettings
        fields = ['new_predictions', 'cappers_predictions', 'dashboard_digests', 'special_offers', 'community_mentions']

class ImageURLWidget(forms.TextInput):
    def format_value(self, value):
        if value:
            return str(value.url)
        return ''

class ProfileForm(forms.ModelForm):
    profile_photo = forms.ImageField(widget=ImageURLWidget, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])], required=False)

    class Meta:
        model = Profile
        fields = ['profile_photo']