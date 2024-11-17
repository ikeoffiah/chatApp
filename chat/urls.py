from django.urls import path
from .views import MessageView

urlpatterns = [
    path('messages/<str:room_name>/', MessageView.as_view(), name='message_api'),
]