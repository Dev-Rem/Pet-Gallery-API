from django.urls import path

from chats.views import MessagesInbox, MessageThread, SendMessage


urlpatterns = [
    path("inbox/", MessagesInbox.as_view()),
    path("thread/<receiver_id>/", MessageThread.as_view()),
    path("send/", SendMessage.as_view()),
]
