import threading
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
import pyotp
from authentication.models import User



def generate_send_otp():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=300)
    otp = totp.now()
    return {'secret': secret, 'otp': otp}

class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        return self.email.send()


def send_email_verification(subject, pin, name, email):
    print('herere')
    print(subject, pin, name, email)
    subject = f'{subject}'
    body = render_to_string(
        'authentications/verify_email.html', {

            'name':name,
            'pin': pin
        }
    )
    email = EmailMultiAlternatives(subject=subject,from_email='ChatApp <support@plastikcards.com>', to=[email])
    email.attach_alternative(body,'text/html')
    EmailThread(email).start()


def send_password_change_email_verification(subject, pin, name, email):
    print('herere')
    print(subject, pin, name, email)
    subject = f'{subject}'
    body = render_to_string(
        'authentications/password_change.html', {

            'name':name,
            'pin': pin
        }
    )
    email = EmailMultiAlternatives(subject=subject,from_email='ChatApp <support@plastikcards.com>', to=[email])
    email.attach_alternative(body,'text/html')
    EmailThread(email).start()


def resend_email_verification(subject, pin, email):
    print('herere')
    print(subject, pin, email)
    subject = f'{subject}'
    body = render_to_string(
        'authentications/resend_otp.html', {

            'pin': pin
        }
    )
    email = EmailMultiAlternatives(subject=subject,from_email='Plastikcards <support@plastikcards.com>', to=[email])
    email.attach_alternative(body,'text/html')
    EmailThread(email).start()


def success_message_helper(data,message):
    return {
        'data':data,
        'detail':message
    }


def error_message_structure(error,message):
    return {
        'error':error,
        'detail':message
    }

def error_message_helper(errors):
    error_message = ""
    print(errors)
    for key, value in errors.items():

        if isinstance(value, list):
            error_message = error_message + f'{value[0]} \n'
        elif isinstance(value, dict):
            for key, valuez in value.items():
                error_message = error_message + f'{valuez[0]} \n'
        else:
            error_message = error_message + f'{value},'
    return error_message_structure(errors,error_message)


def verify_otp(secret_key, otp, validity=300):
    totp = pyotp.TOTP(secret_key, interval=validity)
    return totp.verify(otp)


def user_exist(email):
    user = User.objects.filter(email=email)
    return user.exists()

def get_first_name(email):
    user = User.objects.get(email=email)
    return user.first_name

def get_last_name(email):
    user = User.objects.get(email=email)
    return user.last_name