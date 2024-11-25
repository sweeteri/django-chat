# privatemessages/consumers.py
import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import DirectMessage

class PersonalMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        self.current_user = self.scope['user']

        if self.current_user.is_anonymous:
            await self.close()
        else:

            self.room_group_name = f"direct_{min(self.current_user.id, self.other_user_id)}_{max(self.current_user.id, self.other_user_id)}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Удаляем пользователя из группы WebSocket
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        recipient_id = data['recipient_id']

        recipient = await sync_to_async(User.objects.get)(id=recipient_id)

        # Сохраняем сообщение в базе данных
        new_message = await sync_to_async(DirectMessage.objects.create)(
            sender=self.current_user,
            recipient=recipient,
            content=message
        )

        # Отправляем сообщение в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': new_message.content,
                'sender': new_message.sender.username,
                'recipient': new_message.recipient.username,
                'timestamp': new_message.date_added.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'recipient': event['recipient'],
            'timestamp': event['timestamp']
        }))
