from users.models import Account, CustomUser
from users.serializers import (
    AccountCreateSerializer,
    UserRegisterSerializer,
    UserLoginSerilaizer,
)
from rest_framework import generics, status
from rest_framework.response import Response


class UserRegisterView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"status": "Account registration failed."},
            status=status.HTTP_400_BAD_REQUEST,
        )


# class AccountLoginView(generics.CreateAPIView):

#     queryset = Account.objects.all()
#     serializer_class = AccountLoginSerilaizer
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(
#             {
#                 "status": "Login failed. Please check the username and password provided."
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )
