from rest_framework import serializers
from .models import User
from .utils import *
from core.utils import verify_otp, user_exist


class RegistrationSerializer(serializers.ModelSerializer):
    tokens = serializers.CharField(max_length=100, min_length=6, read_only=True)
    password = serializers.CharField(write_only=True, max_length=100, min_length=4, required=True)

    class Meta:
        model = User
        fields = ['phone_number','email', 'first_name', 'last_name', 'password', 'tokens']

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')

        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('Phone number already exists')

        if len(phone_number) != 10:
            raise serializers.ValidationError('Phone number is invalid')

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            email = validated_data['email'],
            first_name= validated_data['first_name'],
            last_name=validated_data['last_name'],
            password= validated_data['password'],
        )
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    tokens = serializers.CharField(max_length=100, min_length=6, read_only=True)
    password = serializers.CharField(write_only=True, max_length=100, min_length=4, required=True)

    class Meta:
        model = User
        fields = ['email', 'tokens', 'password']

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email or Password is invalid')

        if not active_user_verification(email):
            raise serializers.ValidationError('You have not verified your email')

        if not authenticate_user_with_password(email, password):
            raise serializers.ValidationError('Email of Password is invalid')

        user = User.objects.get(email = email)

        return {
            "token": get_user_token(email),
            "first_name": user.first_name,
            "last_name": user.last_name
        }


class OTPVerificationSerializer(serializers.Serializer):
    secret = serializers.CharField()
    otp = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, attrs):
        secret = attrs.get('secret', None)
        otp = attrs.get('otp', None)
        email = attrs.get('email', None)

        is_valid = verify_otp(secret, otp)

        if not is_valid:
            raise serializers.ValidationError('otp is invalid or expired')

        user = User.objects.filter(email=email)
        if not user.exists():
            raise serializers.ValidationError('Verification failed')

        else:
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()

        return attrs

class ResendOTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email', None)

        if not user_exist(email):
            raise serializers.ValidationError('User is not registered')

        user = User.objects.get(email=email)

        if user.is_active:
            raise serializers.ValidationError("User account is already validated")

        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email', None)

        if not user_exist(email):
            raise serializers.ValidationError('User is not registered')

        return attrs





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']
