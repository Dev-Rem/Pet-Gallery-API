from rest_framework import serializers
from users.serializers import UserInfoSerializer, AccountInfoSerializer
from chats.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    sender = UserInfoSerializer()
    receiver = UserInfoSerializer()

    class Meta:
        model = Chat
        exclude = ["id"]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserInfoSerializer()
    receiver = UserInfoSerializer()
    sender_account = AccountInfoSerializer()
    receiver_account = AccountInfoSerializer()

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
