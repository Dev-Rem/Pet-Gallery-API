from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from posts.models import Hashtag, Post, SavePost, ArchivePost
from users.models import CustomUser
from posts.serializers import (
    PostSerializer,
    ImageSerializer,
    ArchivePostSerializer,
    SavePostSerializer,
)
from utils.permissions import IsOwner

# things to be done


class PostView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.filter(
                user=request.user, is_archived=False, is_deleted=False
            )
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "Something went wrong please try again"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=request.data["id"])
            if post.user == request.user:
                if post.is_archived:
                    archive_obj = ArchivePost.objects.get(user=request.user, post=post)
                    archive_obj.delete()
                    post.is_archived = False
                post.is_deleted = True
                post.save()
                return Response(
                    {"message": "Post deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {"message": "You can not perform this action"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except:
            return Response(
                {"message": "Something went wrong please try again"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=request.data["id"])

            post.caption = request.data["caption"]
            post.location = request.data["location"]

            new_tagged_users = CustomUser.objects.filter(
                username__in=request.data["tags"]
            )
            post.tags.set(new_tagged_users)

            if request.data["hashtags"] == []:
                post.hashtags.clear()
            else:
                post.hashtags.clear()
                post_hashtags = [
                    Hashtag.objects.get_or_create(name=hashtag)[0].id
                    for hashtag in request.data["hashtags"]
                ]
                post.hashtags.add(*post_hashtags)

            post.save()
            # serializer data and return Response
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except:
            return Response(
                {"message": "Something went wrong pelase try again"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, *args, **kwargs):
        try:
            # create a post object
            post = Post.objects.create(
                caption=request.data["caption"],
                location=request.data["location"],
                user=request.user,
            )

            # get and add the users tagged to the post
            if request.data["tags"] != "":
                tagged_users = [
                    CustomUser.objects.get(username=tagged_user)
                    for tagged_user in request.data["tags"].split(",")
                ]
                post.tags.add(*tagged_users)

            # get or create hashtags and add to the post
            if request.data["hashtags"] != "":
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
                archive_obj = ArchivePost.objects.create(user=request.user, post=post)
                post.is_archived = True
                post.save()
                serializer = ArchivePostSerializer(archive_obj)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"message": "You can not perform this action"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        except:
            return Response(
                {"message": "Something went wrong please try again"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SavePostView(generics.GenericAPIView):
    queryset = SavePost.objects.all()
    serializer_class = SavePostSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, *args, **kwargs):
        try:
            user_save_post_obj, created = SavePost.objects.get_or_create(
                user=request.user
            )
            user_save_post_obj.posts.add(request.data["id"])
            serializer = SavePostSerializer(user_save_post_obj)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        except KeyError:
            return Response(
                {"message": "Missing 'id' field in request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "Something went wrong. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request, *args, **kwargs):
        try:
            saved_posts_objs = SavePost.objects.get(user=request.user)
            serializer = SavePostSerializer(saved_posts_objs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "Something went wrong. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, *args, **kwargs):
        try:
            saved_posts_objs = SavePost.objects.get(user=request.user)
            saved_posts_objs.posts.remove(request.data["id"])
            serializer = SavePostSerializer(saved_posts_objs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KeyError:
            return Response(
                {"message": "Missing 'id' field in request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "Something went wrong. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
