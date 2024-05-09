from rest_framework import serializers
from users.serializers import UserInfoSerializer, AccountInfoSerializer
from chats.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        exclude = ["id"]


class MessageSerializer(serializers.ModelSerializer):
    receiver = UserInfoSerializer()
    sender = UserInfoSerializer()
    receiver_account = AccountInfoSerializer()
    sender_account = AccountInfoSerializer()

    class Meta:
        model = Chat
        fields = [
            "sender",
            "sender_account",
            "receiver",
            "receiver_account",
            "is_read",
            "is_edited",
            "message",
            "conversation_code",
        ]
