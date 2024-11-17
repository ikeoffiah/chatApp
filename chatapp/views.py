from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Chat, Messages
from .serializers import ChatProfileSerializerV1, MessageSerializerV1, MessageUserSerializerV1
from .pusher import pusher_client
from core.utils import success_message_helper, error_message_helper, resend_email_verification, send_email_verification, \
    generate_send_otp, verify_otp, send_password_change_email_verification, get_first_name


# View for retrieving the chat profiles for a given user (by user ID)
class ChatProfileViewV1(generics.GenericAPIView):
    queryset = Chat.objects.all()  # Required by GenericAPIView for queryset reference
    serializer_class = ChatProfileSerializerV1  # Use the ChatProfileSerializerV1 for serialization

    # GET method to fetch chats where the user is either person_1 or person_2
    def get(self, request, pk):
        # Filter chats by matching the user ID (person_1 or person_2)
        chats = Chat.objects.filter(Q(person_1=pk) | Q(person_2=pk))
        # Serialize the filtered chat instances
        serializer = self.get_serializer(chats, many=True)
        # Return the serialized data as the response
        return Response(
            success_message_helper(serializer.data ,"",),
        status = status.HTTP_200_OK
        )


# View for posting a new message to a chat
class MessageViewV1(generics.GenericAPIView):
    serializer_class = MessageUserSerializerV1  # Use MessageUserSerializerV1 for message serialization

    # POST method to create a new message and trigger a push notification
    def post(self, request):
        # Initialize the serializer with the incoming request data
        serializer = self.get_serializer(data=request.data)

        # Check if the data is valid according to the serializer
        if serializer.is_valid():
            # Save the valid data (this will create the new message in the database)
            serializer.save()

            # Trigger a push notification to the relevant chat using Pusher
            pusher_client.trigger(
                serializer.validated_data['chat_id'],  # The chat ID
                serializer.validated_data['receiver'],  # The receiver's identifier
                {
                    "sender": serializer.validated_data['sender'],  # Sender of the message
                    "receiver": serializer.validated_data["receiver"],  # Receiver of the message
                    "msg": serializer.validated_data['message'],  # The actual message content
                }
            )
            # Return the serialized message data with a success status
            return Response(
            success_message_helper(serializer.data ,"",),
        status = status.HTTP_200_OK
        )

        # If the data is invalid, return the errors with a bad request status
        return Response(error_message_helper(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


# View for retrieving messages in a specific chat
class ChatViewV1(generics.GenericAPIView):
    queryset = Messages.objects.all()  # Required by GenericAPIView to specify queryset
    serializer_class = MessageSerializerV1  # Use MessageSerializerV1 for message serialization

    # GET method to retrieve all messages for a specific chat identified by the chat_id
    def get(self, request, pk):
        try:
            # Try to fetch the chat by its chat_id
            chat = Chat.objects.get(chat_id=pk)
        except Chat.DoesNotExist:
            # If the chat is not found, return a 404 error with a message
            return Response({"error": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

        # If the chat is found, get all messages related to this chat
        messages = Messages.objects.filter(chat=chat)
        # Serialize the messages
        serializer = self.get_serializer(messages, many=True)
        # Return the serialized messages as the response
        return Response(
            success_message_helper(serializer.data ,"",),
        status = status.HTTP_200_OK
        )
