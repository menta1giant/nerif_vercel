from django.urls import path, include
from users import views

urlpatterns = [
    path('sign-up/create-account', views.CreateUserView.as_view(), name='create-account'),
    path('sign-up/set-up-plan', views.SignupPaymentInfo.as_view(), name='signup-payment-info'),
    path('sign-up/complete', views.SignupPersonalInfo.as_view()),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('login', views.LoginView.as_view(), name='login'),
    path('profile/subscription-info', views.SubscriptionInfo.as_view(), name='subscription-info'),
    path('profile/personal-info', views.PersonalInfo.as_view(), name='personal-info'),
    path('profile/change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('profile/payment-info', views.PaymentInfo.as_view(), name='payment-info'),
    path('profile/localization-info', views.LocalizationInfo.as_view(), name='localization-info'),
    path('profile/notification-settings', views.NotificationSettings.as_view(), name='notification-settings'),
]
