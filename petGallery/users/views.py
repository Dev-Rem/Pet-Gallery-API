from users.models import (
    Account,
    CustomUser,
    SecurityQuestion,
    FollowAccount,
    BlockAccount,
    FollowRequest,
)
from users.serializers import (
    UserRegisterSerializer,
    AccountInfoSerializer,
    AccountUpdateSerializer,
    ChangePasswordSerializer,
    SecurityQuestionSerializer,
    ResetPasswordSerialzer,
    FollowAccountSerializer,
    BlockAccountSerializer,
)
from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)


class UserRegisterView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"status": "Account registration failed."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountInfoSerializer
    permission_classes = [IsAuthenticated]


class AccountInfoView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve the account object for the authenticated user
        return get_object_or_404(Account, user=self.request.user)

    def get(self, request, *args, **kwargs):
        try:
            account = self.get_object()
            serializer = AccountInfoSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AccountUpdateView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve the account object for the authenticated user
        return get_object_or_404(Account, user=self.request.user)

    def put(self, request, *args, **kwargs):
        try:
            account = self.get_object()
            serializer = AccountUpdateSerializer(account, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"detail": "Password has been updated successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordSerialzer

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"detail": "Password has been updated successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateSecurityQuestionView(generics.CreateAPIView):
    queryset = SecurityQuestion.objects.all()
    serializer_class = SecurityQuestionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"status": "Failed to set security"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class FollowAccountView(generics.GenericAPIView):
    queryset = FollowAccount.objects.all()
    serializer_class = FollowAccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the current user
        user = CustomUser.objects.get(username=request.user)

        # Get the list of users that the current user is following
        following_users = FollowAccount.objects.filter(
            follower=user.account
        ).values_list("following", flat=True)
        following_users = Account.objects.filter(id__in=following_users)
        following_users_serializer = AccountInfoSerializer(following_users, many=True)

        # Get the list of users that are following the current user
        followers = FollowAccount.objects.filter(following=user.account).values_list(
            "follower", flat=True
        )
        followers = Account.objects.filter(id__in=followers)
        followers_serializer = AccountInfoSerializer(followers, many=True)

        return Response(
            {
                "followers": followers_serializer.data,
                "following": following_users_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        follower_account = Account.objects.get(user=request.user)

        try:
            following_user = CustomUser.objects.get(
                username=request.data.get("username")
            )
            following_account = Account.objects.get(user=following_user.id)
            if follower_account.id == following_account.id:
                return Response(
                    {"error": "You can not follow yourself"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Account.DoesNotExist:
            return Response(
                {"error": f"{request.data.get('username')} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if the UserFollowing object already exists
        if FollowAccount.objects.filter(
            follower=follower_account.id, following=following_account.id
        ).exists():
            return Response(
                {"error": f"{following_user} is already being followed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the UserFollowing object
        user_following_data = {
            "follower": follower_account.id,
            "following": following_account.id,
        }
        serializer = FollowAccountSerializer(data=user_following_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        follower_account = Account.objects.get(user=request.user.id)

        # Get the user to be unfollowed
        try:
            following_user = CustomUser.objects.get(
                username=request.data.get("username")
            )
            following_account = Account.objects.get(user=following_user.id)
            if follower_account.id == following_account.id:
                return Response(
                    {"error": "You can not unfollow yourself"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Account.DoesNotExist:
            return Response(
                {"error": f"{request.data.get('username')} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if the user is already being followed
        try:
            user_following = FollowAccount.objects.get(
                follower=follower_account, following=following_account
            )
        except FollowAccount.DoesNotExist:
            return Response(
                {"error": "User is not being followed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Unfollow the user
        user_following.delete()

        return Response(
            {"message": "Successfully unfollowed user."}, status=status.HTTP_200_OK
        )


class BlockAccountView(generics.GenericAPIView):

    # https://stackoverflow.com/questions/60338122/in-django-any-user-can-block-any-user-if-they-are-blocked-they-cant-see-the-po
    queryset = BlockAccount.objects.all()
    serializer_class = BlockAccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the current user
        current_user = request.user

        # Get the account associated with the current user
        try:
            user_account = Account.objects.get(user=current_user)
        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Get the blocked users for the current user
        blocked_users = BlockAccount.objects.filter(user=user_account)

        # Serialize the blocked users
        serializer = BlockAccountSerializer(blocked_users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
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
        # user and account objects that wants to block another user
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
