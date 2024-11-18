# Django ChatApp

A simple Django-based ChatApp that allows users to register, log in, send messages, and retrieve past conversations. The app provides RESTful API endpoints for authentication and chat functionalities.

## Features

- User registration and login
- OTP verification for login and password recovery
- Sending and receiving messages between users
- Retrieving previous chat profiles and messages

## Installation

1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd <repo_directory>

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

Pusher was used for real-time delivery
Phone number should be 10 digits

## Base URLs

- **Admin Panel**: `/admin/`
- **Authentication**: `/api/v1/auth/`
- **Chat**: `/api/v1/chat/`
- **Message**: `/api/v1/message/`

## Authentication Endpoints

- **POST** `/api/v1/auth/register`: Register a new user
- **POST** `/api/v1/auth/login`: Login a user
- **POST** `/api/v1/auth/verify-otp`: Verify OTP for login
- **POST** `/api/v1/auth/resend-otp`: Resend OTP for login
- **POST** `/api/v1/auth/forgot-password`: Request password reset
- **GET** `/api/v1/auth/users`: List all users

## Messaging Endpoints

- **GET** `/api/v1/message/chatprofile<str:pk>`: Get all users you've chatted with (use chat_id as `pk`)
- **GET** `/api/v1/message/chat/<str:pk>`: Fetch all messages in a specific chat (use chat_id as `pk`)
- **POST** `/api/v1/message/message`: Send a message

Things I would love to improve 

1. Connect the auth to the chat properly
2. Add uploading of file
3. Group chat
