import logging
from users.models import (
    Account,
    CustomUser,
    FollowAccount,
    BlockAccount,
    FollowRequest,
)
from users.serializers import (
    BlockAccountSerializer,
    FollowRequestSerializer,
    FollowRequestListSerializer,
)
from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


class BlockAccountView(generics.GenericAPIView):

    # https://stackoverflow.com/questions/60338122/in-django-any-user-can-block-any-user-if-they-are-blocked-they-cant-see-the-po
    queryset = BlockAccount.objects.all()
    serializer_class = BlockAccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        This route is for retrieving a list of blocked pets(users).
        """
        # Get the account associated with the current user
        try:
            user_account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Get the blocked users for the current user
        blocked_users = BlockAccount.objects.filter(user=user_account)

        # Check if blocked_users queryset is empty
        if not blocked_users:
            return Response(
                {"message": "No users are blocked."}, status=status.HTTP_200_OK
            )

        # Serialize the blocked users
        serializer = BlockAccountSerializer(blocked_users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        This route is for blocking  a pet(user) account.
        Only need to send the username of the pet(user) to be blocked like this:
        {
            usernmae: String
        }
        """
        # user and account objects that wants to block another user
        user_account = Account.objects.get(user=request.user)

        # check if the user to be blocked exists
        try:
            blocking_user = CustomUser.objects.get(
                username=request.data.get("username")
            )
            blocking_user_account = Account.objects.get(user=blocking_user.id)
        except Account.DoesNotExist:
            return Response(
                {"error": "Account does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            with transaction.atomic():
                # Get or create AccountBlocked object for user_account
                account_blocked, created = BlockAccount.objects.get_or_create(
                    user=user_account
                )

                if blocking_user_account not in account_blocked.users.all():
                    # Remove following if exists
                    following_query = FollowAccount.objects.filter(
                        follower=user_account, following=blocking_user_account
                    )
                    if following_query.exists():
                        following_query.delete()

                    # Remove follower if exists
                    follower_query = FollowAccount.objects.filter(
                        follower=blocking_user_account, following=user_account
                    )
                    if follower_query.exists():
                        follower_query.delete()

                    # Add user to blocked users
                    account_blocked.users.add(blocking_user_account)

                    return Response(
                        {"message": "User has been blocked."},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {"error": "User is already blocked."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        except Exception as e:
            logger.error("Failed to block user: %s", str(e))
            return Response(
                {"error": "Failed to block user."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, *args, **kwargs):
        """
        This route is for unblocking another pet(user).
        Only need to send the username of the pet(user) to be unblocked like this:
        {
            usernmae: String
        }
        """
        # user and account objects that wants to unblock another user
        user_account = Account.objects.get(user=request.user)

        # check if the user to be blocked exists
        try:
            unblocking_user = CustomUser.objects.get(
                username=request.data.get("username")
            )
            unblocking_user_account = Account.objects.get(user=unblocking_user.id)
        except Account.DoesNotExist:
            return Response(
                {"error": "Account does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Add the user to the blocked list
        account_unblocked, created = BlockAccount.objects.get_or_create(
            user=user_account
        )
        if unblocking_user_account in account_unblocked.users.all():
            account_unblocked.users.remove(unblocking_user_account)
            return Response(
                {"message": "User has been unblocked."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "User is already blocked."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class FollowRequestSentView(generics.ListAPIView):
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        This route is for retrieving all follow requests sent to the aunthenticated pet(user).
        """
        account = Account.objects.get(user=request.user)
        follow_requests = FollowRequest.objects.filter(
            request_from=account, status="PENDING"
        )

        if not follow_requests:
            # If there are no follow requests, return an empty list
            return Response(
                {"message": "You do not have any follow requests"},
                status=status.HTTP_200_OK,
            )

        serializer = FollowRequestListSerializer(follow_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowRequestView(generics.GenericAPIView):

    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        account = Account.objects.get(user=request.user)
        follow_requests = FollowRequest.objects.filter(
            request_to=account, status="PENDING"
        )

        if not follow_requests:
            # If there are no follow requests, return an empty list
            return Response([], status=status.HTTP_200_OK)

        serializer = FollowRequestListSerializer(follow_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        This route is for sending follow request to another pet(user).
        Only need to send the username of the pet(user) that is being requested to be followed like this:
        {
            usernmae: String
        }
        """
        account = Account.objects.get(user=request.user)

        try:
            request_to_user = CustomUser.objects.get(
                username=request.data.get("username")
            )
            request_to = Account.objects.get(user=request_to_user.id)
            if request_to.private == False:
                return Response(
                    {
                        "message": "You can not send a follow request to an account that is not private."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if account.id == request_to.id:
                return Response(
                    {"message": "You can not send a follow request to yourself"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Account.DoesNotExist:
            return Response(
                {"error": f"{request.data.get('username')} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        follow_request_data = {
            "request_from": account.id,
            "request_to": request_to.id,
        }
        serializer = FollowRequestSerializer(data=follow_request_data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Request sent successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        This route is for accepting or rejecting a follow request recieved from another pet(user).
        Only need to send the username of the pet(user) that is being accepted or declined like this:
        {
            usernmae: String
        }
        """
        user_account = Account.objects.get(user=request.user)

        try:
            request_user = CustomUser.objects.get(username=request.data.get("username"))
            request_account = Account.objects.get(user=request_user.id)

            if user_account.id == request_account.id:
                return Response(
                    {"error": "You can not accept a follow request from yourself"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            follow_request = FollowRequest.objects.get(
                request_from=request_account, request_to=user_account
            )

            if request.data.get("action") == "accept":
                accept_follow = FollowAccount.objects.create(
                    follower=request_account, following=user_account
                )

                follow_request.status = "ACCEPTED"
                follow_request.save()
                accept_follow.save()
                return Response(
                    {"message": "Follow request accepted"},
                    status=status.HTTP_200_OK,
                )
            else:
                follow_request.status = "DECLINED"
                follow_request.save()
                return Response(
                    {"message": "Follow request declined"},
                    status=status.HTTP_200_OK,
                )

        except Account.DoesNotExist:
            return Response(
                {"error": f"{request.data.get('username')} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, *args, **kwargs):
        """
        This route is for cancelling a request already sent to another pet(user).
        Only need to send the username of the pet(user) that was sent a follow request like this:
        {
            usernmae: String
        }
        """
        user_account = Account.objects.get(user=request.user)

        try:
            # Get the user to whom the follow request was sent
            request_user = CustomUser.objects.get(username=request.data.get("username"))
            request_account = Account.objects.get(user=request_user.id)

            # Check if a follow request exists from the current user to the target user
            try:
                sent_request = FollowRequest.objects.get(
                    request_from=user_account, request_to=request_account
                )
                sent_request.delete()
                return Response(
                    {"message": "Follow request has been cancelled"},
                    status=status.HTTP_200_OK,
                )
            except FollowRequest.DoesNotExist:
                return Response(
                    {"message": "Follow request does not exist"},
                    status=status.HTTP_200_OK,
                )

        except Account.DoesNotExist:
            return Response(
                {"error": f"{request.data.get('username')} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
