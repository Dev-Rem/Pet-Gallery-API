from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db.models import Subquery, OuterRef, Q
from chats.models import Chat
from users.models import CustomUser
from chats.serializers import ChatSerializer, MessageSerializer

# Create your views here.


class MessagesInbox(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        messages = Chat.objects.filter(
            id__in=Subquery(
                CustomUser.objects.filter(
                    Q(sender__receiver=user_id) | Q(receiver__sender=user_id)
                )
                .distinct()
                .annotate(
                    last_msg=Subquery(
                        Chat.objects.filter(
                            Q(sender_id=OuterRef("id"), receiver=user_id)
                            | Q(receiver_id=OuterRef("id"), sender=user_id)
                        )
                        .order_by("-id")[:1]
                        .values_list("id", flat=True)
                    )
                )
                .values_list("last_msg", flat=True)
            )
        ).order_by("-id")
        return messages


class MessageThread(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        sender_id = self.request.user.id
        receiver_id = self.kwargs["receiver_id"]
        messages = Chat.objects.filter(
            sender__in=[sender_id, receiver_id],
            receiver__in=[sender_id, receiver_id],
        )
        return messages


class SendMessage(generics.GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """ """
        try:
            chat_data = {
                "sender": request.user.id,
                "receiver": request.data["receiver_id"],
                "message": request.data["message"],
                "conversation_code": request.data["conversation_code"],
            }
            serializer = self.serializer_class(data=chat_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                {"message": "Something went wrong please try again."},
                status=status.HTTP_404_NOT_FOUND,
            )

    # def put(self, request, *args, **kwargs):
