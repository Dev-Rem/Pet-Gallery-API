from users.models import Account
from users.serializers import AccountRegistrationSerializer
from rest_framework import generics, status
from rest_framework.response import Response


class UserRegistrationView(generics.CreateAPIView):
    """
    A simple ViewSet for listing or retrieving users.
    """

    queryset = Account.objects.all()
    serializer_class = AccountRegistrationSerializer
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
