from core.utils import success_message_helper, error_message_helper, resend_email_verification, send_email_verification, \
    generate_send_otp, verify_otp, send_password_change_email_verification, get_first_name
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer


class UserListView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):

        return User.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)


        return Response(
            success_message_helper(serializer.data ,"",),
        status = status.HTTP_200_OK
        )



# View for user registration
class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer  # Serializer for user registration

    # POST method to handle registration
    def post(self, request):
        data = request.data  # Get the request data
        serializer = self.serializer_class(data=data)  # Initialize the serializer with data

        # Check if the data is valid
        if serializer.is_valid():
            serializer.save()  # Save the new user data to the database
            serializer.validated_data['token'] = eval(serializer.data['tokens'])  # Extract the generated tokens
            del serializer.validated_data['password']  # Remove password from response
            name = serializer.validated_data['first_name']  # Get first name
            email = serializer.validated_data['email']  # Get email

            # Generate OTP for email verification
            get_otp = generate_send_otp()
            serializer.validated_data['secret'] = get_otp['secret']
            serializer.validated_data['otp'] = get_otp['otp']
            # Send verification email (commented out)
            # send_email_verification(subject="Welcome to chatapp 😊", pin=get_otp['otp'], name=name, email=email)

            # Return success message with OTP for verification
            return Response(
                success_message_helper(serializer.validated_data, "Sign Up was successful, verify your account"),
                status=status.HTTP_200_OK)
        # If serializer is invalid, return errors
        return Response(error_message_helper(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


# View for user login
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer  # Serializer for user login

    # POST method to handle login
    def post(self, request):
        data = request.data  # Get the request data
        serializer = self.serializer_class(data=data)  # Initialize the serializer with data

        # Check if the data is valid
        if serializer.is_valid():
            return Response(success_message_helper(serializer.validated_data, "Login was successful"),
                            status=status.HTTP_200_OK)
        # If data is invalid, return errors
        return Response(error_message_helper(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


# View for OTP verification during registration or login
class OTPVerificationView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer  # Serializer for OTP verification

    # POST method to handle OTP verification
    def post(self, request):
        data = request.data  # Get the request data
        serializer = self.serializer_class(data=data)  # Initialize the serializer with data
        if serializer.is_valid():
            email = serializer.validated_data['email']  # Get the email for verification
            return Response(success_message_helper(email, 'Verification successful'), status=status.HTTP_200_OK)
        # If data is invalid, return errors
        return Response(error_message_helper(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


# View for resending OTP for email verification
class ResendOTPVerificationView(generics.GenericAPIView):
    """
        Handles user registration.
        Creates a new user and sends an OTP for email verification.
    """
    serializer_class = ResendOTPVerificationSerializer  # Serializer for resending OTP

    # POST method to handle resending OTP
    def post(self, request):
        data = request.data  # Get the request data
        serializer = self.serializer_class(data=data)  # Initialize the serializer with data
        if serializer.is_valid():
            email = serializer.validated_data['email']  # Get the email for verification

            # Generate OTP for email verification
            get_otp = generate_send_otp()
            serializer.validated_data['secret'] = get_otp['secret']
            serializer.validated_data['otp'] = get_otp['otp']
            # Resend verification email (commented out)
            # resend_email_verification(subject="Complete Your Verification Securely", pin=get_otp['otp'], email=email)

            # Return success message with OTP resent
            return Response(
                success_message_helper(serializer.validated_data, "OTP sent successfully"),
                status=status.HTTP_200_OK)
        # If data is invalid, return errors
        return Response(error_message_helper(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


# View for initiating password reset via OTP
class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer  # Serializer for password reset request

    # POST method to handle forgotten password requests
    def post(self, request):
        data = request.data  # Get the request data
        serializer = self.serializer_class(data=data)  # Initialize the serializer with data
        if serializer.is_valid():
            get_otp = generate_send_otp()  # Generate OTP for password reset
            serializer.validated_data['secret'] = get_otp['secret']
            name = get_first_name()  # Get the first name for email verification
            email = serializer.validated_data['email']  # Get the email for password reset
            serializer.validated_data['otp'] = get_otp['otp']
            # Send password reset verification email (commented out)
            # send_password_change_email_verification(subject="Password Change Authorization", pin=get_otp['otp'], name=name, email=email)

            # Return success message with OTP for password reset
            return Response(
                success_message_helper(serializer.validated_data, "OTP was sent to your email"),
                status=status.HTTP_200_OK)
        # If data is invalid, return errors
        return Response(error_message_helper(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


# View for completing the password change after OTP verification
class CompletePasswordChange(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer  # Serializer for OTP verification during password change

    # POST method to handle completing the password change
    def post(self, request):
        data = request.data  # Get the request data
        serializer = self.serializer_class(data=data)  # Initialize the serializer with data

        # If OTP and password are valid
        if serializer.is_valid():
            email = serializer.data['email']  # Get the email of the user
            password = serializer.data["password"]  # Get the new password

            # Fetch the user from the database and update their password
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()

            # Return success message for password change
            return Response(success_message_helper("", "Password successfully changed"), status=status.HTTP_200_OK)

        # If data is invalid, return errors
        return Response(error_message_helper(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
