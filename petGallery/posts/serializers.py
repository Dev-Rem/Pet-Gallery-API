from rest_framework import serializers
from posts.models import Hashtag, Post, SavedPost, ArchivedPost, Comment, Image


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ["name", " created_at"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image"]


class PostCreateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Post
        fields = ["caption", "location", "images", "hashtags", "tags"]
        extra_kwargs = {
            "location": {"required": False},
            "hashtags": {"required": False},
            "tags": {"required": False},
            "images": {"required": False},
        }


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "user",
            "caption",
            "location",
            "is_deleted",
            "likes",
            "hashtags",
            "date_posted",
        ]


class SavedpostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = ["user", "post", "saved_at"]


class ArchivedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivedPost
        fields = ["user", "post", "archived_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["post", "user", "text", "is_deleted", "comment_date"]
