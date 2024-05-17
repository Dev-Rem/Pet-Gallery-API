from django.urls import path

from chats.views import MessagesInbox, MessageThread


urlpatterns = [
    path("inbox/", MessagesInbox.as_view()),
    path("thread/<sender_id>/<receiver_id>/", MessageThread.as_view()),
]
