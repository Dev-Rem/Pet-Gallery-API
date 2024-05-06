from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from posts.models import Post, Comment
from users.models import Account
from posts.serializers import PostSerializer, CommentSerializer
from utils.permissions import IsOwner


# things to be don
# how to get post and comments in one response object


class FeedPostsView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        """
        This route is for getting posts for the pet(user) feed, this are posts from accounts the pet(user) follows.
        """
        try:
            # get the requesting users account obj and get the usernames of the account the user follows
            user_account = Account.objects.get(user=request.user)
            following_usernames = [
                following.following.user.username
                for following in user_account.following.all()
            ]
            # get posts based on following_usernames, serialize and return Response
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
        """
        This route is for getting posts for the explore feed
        """
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
        """
        This route is for getting all the post the pet(user) has been tagged in
        """
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
        """
        This route is for the user to remove themself from the tag list of a post
        {
            "id": post_id
        }
        """
        try:
            # get the post obj and check if the user is in the tag list
            post = Post.objects.get(id=request.data["id"])
            if request.user in post.tags.all():
                # remove user from tag list, save post obj, and return Response
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
        """
        This route is for getting posts that the pet(user has liked)
        """
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
        """
        This route is for liking and unliking a post
        {
            "id": post_id
        }
        """
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
        """
        This route is for getting all the comments fo a post and its replies
        {
            "id": post_id
        }
        """
        try:
            post = Post.objects.get(id=request.data["id"])
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
        """
        This route is for creating a comment and also replying to a comment
        for comments
        {
            "post": post_id
        }
        for replies
        {
            "comment": comment_id
        }
        """
        try:
            # check if post id was sent in request data if not then it is a reply to a comment
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
        """
        This route is for editing comments the pet(user) has created
        {
            "id": comment_id
        }
        """
        try:
            # get the comment object and check if the pet(user) is the owner of the comment obj, then assign new text value.
            comment = Comment.objects.get(id=request.data["id"])
            if request.user == comment.user:
                comment.text = request.data["text"]
                # change the edited flag to True to show it was edited, save comment obj, and return Response
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
        """
        This route is for a pet(user) to like and unlike a comment or reply
        {
            "id": comment_id
        }
        """
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
        """
        This route is for deleting a comment
        {
            "id": comment_id
        }
        """
        try:
            # get the comment obj and check if the pet(user) is the owner of the comment or the owner of the post
            comment = Comment.objects.get(id=request.data["id"])
            if (request.user == comment.user) or (request.user == comment.post.user):
                # set the is_deleted flag of the comment to True, save, and return Response
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
