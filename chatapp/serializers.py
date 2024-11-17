from rest_framework import serializers
from .models import Chat, Messages


# Serializer for the Chat model
class ChatSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Chat
        # Only include the 'chat_id' field in the serialized output
        fields = ('chat_id',)


# Serializer for the Messages model
class MessageSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Messages
        # Exclude the 'id' field from the serialized output
        exclude = ('id',)


# Serializer for Chat with the related messages
class ChatProfileSerializerV1(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()  # Custom field for related messages

    class Meta:
        model = Chat
        fields = ('chat_id', 'messages')  # Include chat_id and the custom messages field

    # Method to retrieve the latest message for each chat
    def get_messages(self, obj):
        # Get the chat instance based on the current object
        chat = Chat.objects.get(id=obj.id)
        # Get the last message related to the current chat
        message = [Messages.objects.filter(chat=chat).last()]
        # Serialize the message(s) using the MessageSerializerV1
        return MessageSerializerV1(message, many=True).data


# Serializer for Messages including user-specific fields
class MessageUserSerializerV1(serializers.ModelSerializer):
    chat_id = serializers.CharField()  # Chat ID field
    person_1 = serializers.CharField(required=False)  # Person 1 (optional)
    person_2 = serializers.CharField(required=False)  # Person 2 (optional)

    class Meta:
        model = Messages
        # Include these fields in the serialized output
        fields = ('sender', 'receiver', 'message', 'message_time', 'chat_id', 'person_1', 'person_2')

    # Validation method to check if the chat exists or needs to be created
    def validate(self, attrs):
        chat_id = attrs['chat_id']
        # Check if a chat with the given chat_id already exists
        chat = Chat.objects.filter(chat_id=chat_id).exists()

        # If the chat does not exist, create a new chat with person_1 and person_2
        if not chat:
            person_1 = attrs['person_1']
            person_2 = attrs['person_2']
            Chat.objects.create(chat_id=chat_id, person_1=person_1, person_2=person_2)

        # Return the validated attributes
        return attrs

    # Create method to associate the validated data with a specific chat instance
    def create(self, validated_data):
        # Extract chat_id from the validated data
        chat_id = validated_data.pop('chat_id', None)
        person_1 = validated_data.pop('person_1', None)
        person_2 = validated_data.pop('person_2',None)

        # Get the chat instance using the chat_id
        chat = Chat.objects.get(chat_id=chat_id)
        # Associate the chat instance with the validated message data
        validated_data['chat'] = chat

        # Call the parent class's create method to save the message
        return super().create(validated_data)
