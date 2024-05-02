import base64
from rest_framework import serializers
from posts.models import Hashtag, Post, SavedPost, ArchivePost, Comment, Image
from users.models import CustomUser
from users.serializers import UserInfoSerializer


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    images = ImageSerializer(many=True, read_only=True)
    tags = UserInfoSerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "user",
            "caption",
            "location",
            "tags",
            "hashtags",
            "images",
            "is_deleted",
            "likes",
            "date_posted",
        ]
        depth = 1


class ArchivePostSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    post = PostSerializer()

    class Meta:
        model = ArchivePost
        fields = "__all__"
        depth = 2
