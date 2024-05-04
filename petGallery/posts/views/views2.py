from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from posts.models import Hashtag, Post, SavePost, ArchivePost
from users.models import CustomUser, Account
from posts.serializers import (
    PostSerializer,
    ImageSerializer,
    ArchivePostSerializer,
    SavePostSerializer,
)
from utils.permissions import IsOwner


# things to be don
# Views to handle likes


class FeedPostsView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        try:
            user_account = Account.objects.get(user=request.user)
            following_usernames = [
                following.following.user.username
                for following in user_account.following.all()
            ]

            posts = Post.objects.filter(user__username__in=following_usernames)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "Something went wrong. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExplorePostsView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        try:
            users_accounts = Account.objects.all()
            accounts_usernames = [account.user.username for account in users_accounts]
            posts = Post.objects.filter(user__username__in=accounts_usernames)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "Something went wrong. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TaggedPostsView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.filter(tags__username=request.user)
            serializer = PostSerializer(posts, many=True)
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
            post = Post.objects.get(id=request.data["id"])
            if request.user in post.tags.all():
                post.tags.remove(request.user)
                post.save()
                return Response(
                    {"message": "Tag removed successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response({"message": "You can not perform this action"})

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


class LikePostsView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.filter(likes__username=request.user)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "Something went wrong. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=request.data["id"])
            if request.user not in post.likes.all():
                post.likes.add(request.user)
                return Response({"message": "Liked Post"}, status=status.HTTP_200_OK)
            else:
                post.likes.remove(request.user)
                return Response({"message": "Unliked Post"}, status=status.HTTP_200_OK)

            post.save()
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
