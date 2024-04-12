from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import (
    AuthenticationFailed,
    InvalidToken,
    TokenError,
)
from rest_framework_simplejwt.views import TokenViewBase
from posts.models import Hashtag, Post, SavedPost, ArchivedPost, Comment, Image
from posts.serializers import PostCreateSerializer


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        hashtags_data = request.data.pop("hashtags")
        for hashtag in hashtags_data:
            Hashtag.objects.get_or_create(name=hashtag)

        images_data = request.data.pop("images")
        for image in images_data:
            Image.objects.create(post, image=image)

        # serializer = PostCreateSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
