from rest_framework import serializers
from users.serializers import UserInfoSerializer, AccountInfoSerializer
from chats.models import Chat


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        exclude = ["id"]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserInfoSerializer()
    receiver = UserInfoSerializer()

    class Meta:
        model = Chat
        exclude = ["id"]
