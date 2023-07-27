from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from .image_utils import resize_image
from datetime import datetime, date 
from nerif_vercel.storages import select_storage

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    username = None
    email = models.EmailField(unique=True, db_index=True)

    phone = models.CharField(max_length=25, unique=True, null=True)
    location = models.CharField(max_length=25, null=True)
    currency = models.CharField(max_length=25, null=True)
    card_info = models.CharField(max_length=25, null=True)
    language = models.CharField(max_length=25, null=True)
    timezone = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_photo = models.ImageField(storage=select_storage(), upload_to='profile_images/')

    def save(self, *args, **kwargs):
        deleted = False
        if self.pk:
            saved_image = Profile.objects.get(pk=self.pk).profile_photo
            if saved_image and saved_image != self.profile_photo:
                saved_image.delete(save=False)
                deleted = True
            if not(saved_image): deleted = True
        if deleted and self.profile_photo: self.profile_photo = resize_image(self, self.profile_photo)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class UserNotificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    new_predictions = models.BooleanField(default=True)
    cappers_predictions = models.BooleanField(default=True)
    dashboard_digests = models.BooleanField(default=True)
    special_offers = models.BooleanField(default=True)
    community_mentions = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    period = models.IntegerField(default=0)
    date_started = models.DateField(default=date.today)
    plan = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username