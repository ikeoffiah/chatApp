from .models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


def active_user_verification(email:str):
    user = User.objects.filter(email=email)
    if user.exists():
        user = User.objects.get(email=email)
        return user.is_active
    else:
        return False


def get_user_token(email:str):
    try:
        user = User.objects.get(email=email)
        token = user.tokens()
        return token
    except ObjectDoesNotExist:
        raise ValueError('User does not exist')

def authenticate_user_with_password(email, password):

    user = User.objects.get(email=email)

    if user.check_password(password):
        user.last_login = timezone.now()
        user.save()
        return True
    else:
        return False
