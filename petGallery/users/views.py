from users.models import Account, CustomUser, SecurityQuestion
from users.serializers import (
    UserRegisterSerializer,
    AccountInfoSerializer,
    AccountUpdateSerializer,
    ChangePasswordSerializer,
    SecurityQuestionSerializer,
)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


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
