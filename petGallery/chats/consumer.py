import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from typing import Tuple, Dict

from users.models import CustomUser
from chats.models import Chat


def save_message(
    message: str, current_user_id: int, other_user_id: int, room_name: str
) -> Chat:
    current_user = CustomUser.objects.get(id=current_user_id)
    other_user = CustomUser.objects.get(id=other_user_id)
    instance = Chat.objects.create(
        sender=current_user,
        receiver=other_user,
        message=message,
        conversation_code=room_name,
    )
    instance.save()
    return instance


def min_max(value1, value2) -> Tuple:
    value1 = int(value1)
    value2 = int(value2)
    min_id = min(value1, value2)
    max_id = max(value1, value2)
    return min_id, max_id


class ChatConsumer(WebsocketConsumer):
    def generate_room_name(self):
        other_user_id: int = self.get_other_user_id()
        current_user_id: int = self.get_current_user_id()

        min_id, max_id = min_max(other_user_id, current_user_id)
        room_name = f"user{min_id}_{max_id}chat"
        return room_name

    def get_other_user_id(self):
        return self.scope["url_route"]["kwargs"]["user_id"]

    def get_current_user_id(self):
        return self.scope["auth_user_id"]

    def add_user_to_group(self):
        self.room_name = self.generate_room_name()
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

    def remove_user_from_group(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def save_message(self, message):
        current_user = self.get_current_user_id()
        other_user = self.get_other_user_id()
        instance = save_message(
            message=message,
            current_user_id=current_user,
            other_user_id=other_user,
            room_name=self.room_name,
        )
        return instance

    def process_message(self, message):
        new_message = self.save_message(message)
        return {
            "message": new_message.message,
            "sender": new_message.sender.id,
            "receiver": new_message.receiver.id,
            "created_at": str(new_message.created_at),
        }

    def connect(self):
        self.add_user_to_group()
        self.accept()

    def disconnect(self, close_code):
        self.remove_user_from_group()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        processed_message: Dict = self.process_message(message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {"type": "chat_message", "message": processed_message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
