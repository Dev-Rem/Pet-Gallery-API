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

