from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('sign-up/create-account', views.CreateUserView.as_view()),
    path('sign-up/set-up-plan', views.SignupPaymentInfo.as_view()),
    path('sign-up/complete', views.SignupPersonalInfo.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('login', views.LoginView.as_view()),
    path('profile/subscription-info', views.SubscriptionInfo.as_view()),
    path('profile/personal-info', views.PersonalInfo.as_view()),
    path('profile/change-password', views.ChangePasswordView.as_view()),
    path('profile/payment-info', views.PaymentInfo.as_view()),
    path('profile/localization-info', views.LocalizationInfo.as_view()),
    path('profile/notification-settings', views.NotificationSettings.as_view()),
]
