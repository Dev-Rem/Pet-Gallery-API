from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from posts.models import Hashtag, Post, SavedPost, ArchivePost, Comment, Image
from users.models import CustomUser
from posts.serializers import PostSerializer, ImageSerializer, ArchivePostSerializer
from posts.permissions import IsOwner

# things to be done
# when user deletes a post the archive object should also be deleted


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # create a post object
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

            # get images from request.FILES and create image objects using ImageSerializer
            images = request.FILES.getlist("images")
            for image in images:
                image_serializer = ImageSerializer(
                    data={"post": post.pk, "image": image}
                )
                if image_serializer.is_valid():
                    image_serializer.save()
                else:
                    return Response(
                        image_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            # serializer data and return Response
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except:
            return Response(
                {"message": "Something went wrong pelase try again"},
                status=status.HTTP_204_NO_CONTENT,
            )


class ArchivePostView(generics.GenericAPIView):
    queryset = ArchivePost.objects.all()
    serializer_class = ArchivePostSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        archived_posts = ArchivePost.objects.filter(user=request.user)
        serializer = ArchivePostSerializer(archived_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        This view allows user to add a post from archive
        """
        try:
            # get the post
            post = Post.objects.get(id=request.data["post"])

            if post.user == request.user:
                serializer = ArchivePostSerializer(
                    data={"user": request.user.id, "post": post.id}
                )
                if serializer.is_valid(raise_exception=True):
                    post.is_archived = True
                    post.save()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"message": "You can not perform this action"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        except:
            return Response(
                {"message": "Something went wrong please try again"},
                status=status.HTTP_204_NO_CONTENT,
            )

    def put(self, request, *args, **kwargs):
        """
        This view allows user to remove a post from archive
        """
        try:
            # get the archived post
            archived_post = ArchivePost.objects.get(id=request.data["id"])

            if archived_post.user == request.user:
                post = Post.objects.get(id=archived_post.post.id)
                post.is_archived = False
                post.save()
                archived_post.delete()
                return Response(
                    {"message": "Post removed from archive successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {"message": "You can not perform this action"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        except:
            return Response(
                {"message": "Something went wrong please try again"},
                status=status.HTTP_204_NO_CONTENT,
            )
