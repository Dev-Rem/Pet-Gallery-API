from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db.models import Subquery, OuterRef, Q
from chats.models import Chat
from users.models import CustomUser
from chats.serializers import MessageSerializer, ChatSerializer
from utils.permissions import IsOwner

# Create your views here.


class MessagesInbox(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            messages = Chat.objects.filter(
                id__in=Subquery(
                    CustomUser.objects.filter(
                        Q(sender__receiver=request.user.id)
                        | Q(receiver__sender=request.user.id)
                    )
                    .distinct()
                    .annotate(
                        last_msg=Subquery(
                            Chat.objects.filter(
                                Q(sender_id=OuterRef("id"), receiver=request.user.id)
                                | Q(receiver_id=OuterRef("id"), sender=request.user.id)
                            )
                            .order_by("-id")[:1]
                            .values_list("id", flat=True)
                        )
                    )
                    .values_list("last_msg", flat=True)
                )
            ).order_by("-id")
            serializer = self.serializer_class(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response(
                {"message": "Something went wrong please try again"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MessageThread(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sender_id = self.kwargs["sender_id"]
        receiver_id = self.kwargs["receiver_id"]
        messages = Chat.objects.filter(
            sender__in=[sender_id, receiver_id],
            receiver__in=[sender_id, receiver_id],
        )
        return messages
