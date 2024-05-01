import base64
from rest_framework import serializers
from posts.models import Hashtag, Post, SavedPost, ArchivedPost, Comment, Image
from users.models import CustomUser
from users.serializers import AccountInfoSerializer


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = Image
        fields = ["post", "images"]

    def create(self, validated_data):
        print(self.context)
        post = self.context.get("post")
        print(post)  # Remove 'post' from validated_data
        images = validated_data["images"]
        image_objs = []

        for image in images:
            image_objs.append(Image.objects.create(post=post, image=image))

        return image_objs


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    tags = AccountInfoSerializer(many=True, read_only=True)
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


class PostSerializer(serializers.ModelSerializer):

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
