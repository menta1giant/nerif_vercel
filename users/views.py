from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime
from django.db.models import F, Q
import time

from .forms import PersonalInfoForm, PaymentInfoForm, ChangePasswordForm, LocalizationInfoForm, NotificationSettingsForm, SignupPaymentInfoForm, SignupPlanSetupForm, SignupPersonalInfoForm, ProfileForm
from .models import User, Profile, UserNotificationSettings, Subscription
from .utils import get_user_from_token
from .response import DEFAULT_SUCCESS_MESSAGE
from .serializers import ProfileSerializer, SubscriptionSerializer

from rest_framework import status
from django.contrib.auth import authenticate, login, logout

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class CreateUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email, password)

        token = Token.objects.create(user=user)

        login(request, user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)

            token, _ = Token.objects.get_or_create(user=user)

            return Response({'message': 'Logged in successfully', 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)

        try:
            token = request.auth
            if token:
                token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass

        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    
class SignupPaymentInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.auth
        user_instance = get_user_from_token(token)

        if (not(user_instance)): return Response(400)
        
        form_user = SignupPaymentInfoForm(data=request.data, instance=user_instance)

        user_plan, _ = Subscription.objects.get_or_create(user=user_instance)
        form_plan = SignupPlanSetupForm(data=request.data, instance=user_plan)
        if form_user.is_valid() and form_plan.is_valid():
            user = form_user.save(commit=False)
            user.save()

            plan = form_plan.save(commit=False)
            plan.save()
            return Response(status=200)
        return Response(form_user.errors, status=400)

class SignupPersonalInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.auth
        user_instance = get_user_from_token(token)

        if (not(user_instance)): return Response(status=401)
        profile, _ = Profile.objects.get_or_create(user=user_instance)

        form_profile = ProfileForm(data=request.data, files=request.FILES, instance=profile)
        
        form = SignupPersonalInfoForm(data=request.data, instance=user_instance)

        if form.is_valid() and form_profile.is_valid():
            profile = form_profile.save(commit=False)
            profile.save()

            user = form.save(commit=False)
            user.save()

            return Response({'message': 'Account successfully created'}, status=200)
        return Response(form.errors, status=400)

class SubscriptionInfo(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        token = request.auth
        user_instance = get_user_from_token(token)

        if (not(user_instance)): return Response(status=400)

        user_plan, _ = Subscription.objects.get_or_create(user=user_instance)
        form_serializer = SubscriptionSerializer(user_plan)

        return Response(form_serializer.data, status=status.HTTP_200_OK)
    

class PersonalInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.auth
        user_instance = get_user_from_token(token)

        if (not(user_instance)): return Response(status=400)
        profile, _ = Profile.objects.get_or_create(user=user_instance)

        form_profile = ProfileForm(data=request.data, files=request.FILES, instance=profile)
        
        form = PersonalInfoForm(data=request.data, instance=user_instance)
        if form.is_valid() and form_profile.is_valid():
            profile = form_profile.save(commit=False)
            profile.save()

            user = form.save(commit=False)
            user.save()
            return Response({'message': DEFAULT_SUCCESS_MESSAGE}, status=200)
        return Response({**form.errors, **form_profile.errors, 'message': 'An error occured'}, status=400)
    
    def get(self, request):
        token = request.auth
        user_instance = get_user_from_token(token)

        if (not(user_instance)): return Response(status=400)

        form = PersonalInfoForm(instance=user_instance)
        profile, _ = Profile.objects.get_or_create(user=user_instance)

        serializer_profile = ProfileSerializer(profile)
        data = {field_name: form[field_name].value() for field_name in form.fields}
        data = {**data, **serializer_profile.data}

        return Response(data, status=status.HTTP_200_OK)
        
    
class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        form = ChangePasswordForm(request.data)

        if not(form.is_valid()): return Response({'message': 'Something\'s wrong.'}, status=400)

        old_password = request.data.get('old_password')
        new_password = request.data.get('password')

        token = request.auth
        user_instance = get_user_from_token(token)

        if (not(user_instance)): return Response(status=400)
        
        user = authenticate(username=user_instance.email, password=old_password)

        if user is not None:
            user.set_password(new_password)
            user.save()

            login(request, user)

            return Response({'message': 'Password changed successfully'}, status=200)
        else:
            return Response({'message': 'Please fill in the fields correctly', 'error': 'Invalid old password'}, status=400)
    
class PaymentInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.auth
        user_instance = get_user_from_token(token)

        if (not(user_instance)): return Response(status=400)

        form = PaymentInfoForm(data=request.data, instance=user_instance)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return Response({'message': DEFAULT_SUCCESS_MESSAGE}, status=200)
        return Response({'message': 'Intentionally bad frontend validation has happened'}, status=401)
    
    def get(self, request):
        token = request.auth
        user_instance = get_user_from_token(token)

        if (not(user_instance)): return Response(status=400)

        form = PaymentInfoForm(instance=user_instance)

        data = {field_name: form[field_name].value() for field_name in form.fields}

        return Response(data, status=status.HTTP_200_OK)
    
class LocalizationInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.auth
        user_instance = get_user_from_token(token)

        if (not(user_instance)): return Response(status=400)

        form = LocalizationInfoForm(data=request.data, instance=user_instance)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return Response({'message': DEFAULT_SUCCESS_MESSAGE}, status=200)
        return Response(form.errors, status=400)
    
    def get(self, request):
        token = request.auth
        user_instance = get_user_from_token(token)

        if (not(user_instance)): return Response(status=400)

        form = LocalizationInfoForm(instance=user_instance)

        data = {field_name: form[field_name].value() for field_name in form.fields}

        return Response(data, status=status.HTTP_200_OK)
    
class NotificationSettings(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.auth
        user_instance = get_user_from_token(token)

        if (not(user_instance)): return Response(status=400)

        user_notification_settings, _ = UserNotificationSettings.objects.get_or_create(user=user_instance)

        form = NotificationSettingsForm(data=request.data, instance=user_notification_settings)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return Response({'message': DEFAULT_SUCCESS_MESSAGE}, status=200)
        return Response(form.errors, status=400)
    
    def get(self, request):
        token = request.auth
        user_instance = get_user_from_token(token)

        if (not(user_instance)): return Response(status=400)

        user_notification_settings, _ = UserNotificationSettings.objects.get_or_create(user=user_instance)

        form = NotificationSettingsForm(instance=user_notification_settings)

        data = {field_name: form[field_name].value() for field_name in form.fields}

        return Response(data, status=status.HTTP_200_OK)