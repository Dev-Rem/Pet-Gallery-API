import base64
from rest_framework import serializers
from posts.models import Hashtag, Post, SavePost, ArchivePost, Comment, Image
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
            "id",
            "user",
            "caption",
            "location",
            "tags",
            "hashtags",
            "images",
            "is_deleted",
            "is_archived",
            "likes",
            "created_at",
            "updated_at",
        ]
        depth = 1


class ArchivePostSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    post = PostSerializer()

    class Meta:
        model = ArchivePost
        fields = "__all__"
        depth = 2


class SavePostSerializer(serializers.ModelSerializer):

    user = UserInfoSerializer()
    posts = PostSerializer(many=True)

    class Meta:
        model = SavePost
        fields = "__all__"
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    post = PostSerializer()
    likes = UserInfoSerializer(many=True)

    class Meta:
        model = Comment
        fields = "__all__"
        depth = 1
