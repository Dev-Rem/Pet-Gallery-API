from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from posts.models import Post, Comment
from users.models import Account
from posts.serializers import PostSerializer, CommentSerializer
from utils.permissions import IsOwner


# things to be don
# Views to handle comment replies
# how to get post and comments in one response object


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
                post.save()
                return Response({"message": "Liked Post"}, status=status.HTTP_200_OK)
            else:
                post.likes.remove(request.user)
                post.save()
                return Response({"message": "Unliked Post"}, status=status.HTTP_200_OK)

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


class CommentsView(generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_comments_with_replies(self, post):
        # Fetch all comments related to the post
        comments = Comment.objects.filter(post=post, is_deleted=False)
        # Create a dictionary to hold comments and their replies
        comments_with_replies = {}
        # Iterate over each comment
        for comment in comments:
            # Fetch replies for the current comment
            replies = Comment.objects.filter(replies=comment)
            # Serialize the comment and its replies
            comment_data = CommentSerializer(comment).data
            replies_data = CommentSerializer(replies, many=True).data
            # Add the replies data to the comment data
            comment_data["replies"] = replies_data
            # Add the comment and its replies to the dictionary
            comments_with_replies[comment.id] = comment_data
        return comments_with_replies

    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=request.data["post"])
            comments_with_replies = self.get_comments_with_replies(post)
            return Response(comments_with_replies, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "Something went wrong. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, *args, **kwargs):
        try:
            if "post" in request.data:
                post = Post.objects.get(id=request.data["post"])
                comment = Comment.objects.create(
                    post=post, user=request.user, text=request.data["text"]
                )
                serializer = CommentSerializer(comment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                parent_comment = Comment.objects.get(id=request.data["comment"])
                comment = Comment.objects.create(
                    post=parent_comment.post,
                    user=request.user,
                    text=request.data["text"],
                    replies=parent_comment,
                )
                serializer = CommentSerializer(comment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError:
            return Response(
                {"message": "Some data field is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "Something went wrong. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=request.data["id"])
            if request.user == comment.user:
                comment.text = request.data["text"]
                comment.edited = True
                comment.save()
                serializer = CommentSerializer(comment)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "you can not perform that action"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except KeyError:
            return Response(
                {"message": "Some data field is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "Something went wrong. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=request.data["id"])
            if request.user not in comment.likes.all():
                comment.likes.add(request.user)
                comment.save()
                return Response({"message": "Liked Comment"}, status=status.HTTP_200_OK)
            else:
                comment.likes.remove(request.user)
                comment.save()
                return Response(
                    {"message": "Unliked Comment"}, status=status.HTTP_200_OK
                )

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

    def delete(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=request.data["id"])
            if (request.user == comment.user) or (request.user == comment.post.user):
                comment.is_deleted = True
                comment.save()
                return Response(
                    {"message": "Comment deleted Successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "you can not perform that action"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
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
