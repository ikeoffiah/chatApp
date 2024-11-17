from django.db import models
from datetime import datetime, timezone

class Chat(models.Model):
    chat_id = models.CharField(unique=True, max_length=200)
    person_1 = models.CharField(max_length=100)
    person_2 = models.CharField(max_length=100)

    def __str__(self):
        return f'chat between {self.person_1} and {self.person_2}'


class Messages(models.Model):
    chat = models.ForeignKey(Chat, related_name='chat', on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    message_time = models.DateTimeField( auto_now_add = True, blank=True)

    def __str__(self):
        return f'{self.sender} messaged {self.receiver}'