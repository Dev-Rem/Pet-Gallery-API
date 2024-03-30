import logging
from users.models import (
    Account,
    CustomUser,
    SecurityQuestion,
    FollowAccount,
)
from users.serializers import (
    UserRegisterSerializer,
    AccountInfoSerializer,
    AccountUpdateSerializer,
    ChangePasswordSerializer,
    SecurityQuestionSerializer,
    ResetPasswordSerialzer,
    FollowAccountSerializer,
    CustomTokenObtainPairSerializer,
    InActiveUser,
)

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

logger = logging.getLogger(__name__)


class CustomTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.

    Returns HTTP 406 when user is inactive and HTTP 401 when login credentials are invalid.
    """

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            raise InActiveUser()
        except TokenError:
            raise InvalidToken()

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserRegisterView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
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
        # this route is for updating account information

        try:
            account = self.get_object()
            serializer = AccountUpdateSerializer(account, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        # this route is for changing the account to private
        try:
            account = self.get_object()
            account.private = not account.private
            serializer = AccountUpdateSerializer(
                account, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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

        # Create the FollowAccount object
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
            {"message": "Successfully unfollowed account."}, status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        # this route is used for removing a follower
        user_account = Account.objects.get(user=request.user)

        # Get the follower to be removed
        try:
            follower_user = CustomUser.objects.get(
                username=request.data.get("username")
            )
            follower_account = Account.objects.get(user=follower_user.id)
            if user_account.id == follower_account.id:
                return Response(
                    {"message": "You can not remove yourself as follower"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Account.DoesNotExist:
            return Response(
                {"error": f"{request.data.get('username')} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Remove follower
        try:
            remove_follower = FollowAccount.objects.get(
                follower=follower_account, following=user_account
            )
            remove_follower.delete()
        except:
            return Response(
                {"message": "You need to unfollow the account first"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "Successfully removed follower."}, status=status.HTTP_200_OK
        )
