from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from posts.models import Hashtag, Post, SavedPost, ArchivedPost, Comment, Image
from users.models import CustomUser
from posts.serializers import PostSerializer, ImageSerializer


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            post = Post.objects.create(
                caption=request.data["caption"],
                location=request.data["location"],
                user=request.user,
            )

            # get and add the users tagged to the post
            tagged_users = [
                CustomUser.objects.get(username=tagged_user)
                for tagged_user in request.data["tags"].split(",")
            ]
            post.tags.add(*tagged_users)

            # get or create hashtags and add to the post
            post_hashtags = [
                Hashtag.objects.get_or_create(name=hashtag)[0].id
                for hashtag in request.data["hashtags"].split(",")
            ]
            post.hashtags.add(*post_hashtags)

            # create image objects using ImageSerializer
            image_serializer = ImageSerializer(
                data=request.FILES, context={"post": post}
            )
            if image_serializer.is_valid():
                image_serializer.save()

            # serializer data and return Response
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except:
            return Response(
                {"message": "Something went wrong pelase try again"},
                status=status.HTTP_204_NO_CONTENT,
            )
