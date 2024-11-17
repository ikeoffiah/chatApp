from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer

class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_name):
        messages = Message.objects.filter(room_name=room_name).order_by('-timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, room_name):
        data = request.data
        data['user'] = request.user.id
        data['room_name'] = room_name
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
