from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserManager(BaseUserManager):

    """Custom create user service"""

    def create_user(self, first_name, last_name, email, phone_number, password, **extra_fields):

        if not email:
            raise ValueError('Email must be set')

        if not phone_number:
            raise ValueError('Phone number must be set')


        user_phone_number = User.objects.filter(phone_number=phone_number).exists()
        if user_phone_number:
            raise ValueError('User already exist with this phone number')

        email = self.normalize_email(email)
        user_email_check = User.objects.filter(email=email).exists()
        if user_email_check:
            raise ValueError('User already exist')
        user = self.model(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    """Custom create super user or admin"""
    def create_superuser(self,first_name, last_name, email, phone_number, password, **extra_fields ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser is_staff must be True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))


        return self.create_user( email=email,phone_number=phone_number,first_name=first_name, last_name=last_name,password=password, **extra_fields )








class User(AbstractBaseUser, PermissionsMixin):
    """User model authentication for all type of user authentications"""

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100, unique=True)



    # user status
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def tokens(self):
        refresh_token = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        }
