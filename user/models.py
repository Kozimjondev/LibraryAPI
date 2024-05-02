from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from base.models import BaseModel
from .choices import GENDER
from .managers import UserManager

phone_number_regex = RegexValidator(regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
                                    message="Phone number must be entered in the format: '+998901234567'. "
                                            "Up to 13 digits allowed.'", )


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = None
    first_name = models.CharField(_('First Name'), max_length=50)
    last_name = models.CharField(_('Last Name'), max_length=50)
    email = models.EmailField(_('Email'), unique=True)
    phone_number = models.CharField(_('Phone Number'), max_length=13,
                                    unique=True, validators=[phone_number_regex])
    gender = models.CharField(_('Gender'), max_length=10, choices=GENDER)
    date_of_birth = models.DateField(_('Date of Birth'), blank=True, null=True)
    password = models.CharField(_('Password'), max_length=100)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    is_superuser = models.BooleanField(_('Superuser'), default=False)
    date_joined = models.DateTimeField(_('Date Joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('phone_number',)

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_pair_token(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile', primary_key=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    address = models.CharField(_('Address'), max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        if created:
            UserProfile.objects.create(user=instance).save()
    except Exception as err:
        print(f"Error creating user profile: {err}")
