from django.urls import path
from .views import *

urlpatterns = [
    path('chatprofile<str:pk>',ChatProfileViewV1.as_view()),
    path('chat/<str:pk>',ChatViewV1.as_view()),
    path('message', MessageViewV1.as_view())
]