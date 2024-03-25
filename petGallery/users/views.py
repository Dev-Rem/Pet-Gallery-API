from django.http import Http404
from users.models import Account, CustomUser, SecurityQuestion, AccountFollowing
from users.serializers import (
    UserRegisterSerializer,
    AccountInfoSerializer,
    AccountUpdateSerializer,
    ChangePasswordSerializer,
    SecurityQuestionSerializer,
    ResetPasswordSerialzer,
    AccountFollowingSerializer,
)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework import viewsets


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


class AccountFollowingView(generics.GenericAPIView):
    queryset = AccountFollowing.objects.all()
    serializer_class = AccountFollowingSerializer
    permission_classes = [IsAuthenticated]

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
        if AccountFollowing.objects.filter(
            follower_id=follower_account.id, following_id=following_account.id
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
        serializer = AccountFollowingSerializer(data=user_following_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        follower_account = Account.objects.get(user=request.user)

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
            user_following = AccountFollowing.objects.get(
                follower=follower_account, following=following_account
            )
        except AccountFollowing.DoesNotExist:
            return Response(
                {"error": "User is not being followed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Unfollow the user
        user_following.delete()

        return Response(
            {"message": "Successfully unfollowed user."}, status=status.HTTP_200_OK
        )
