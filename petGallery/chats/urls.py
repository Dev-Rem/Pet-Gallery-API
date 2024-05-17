from django.urls import path

from chats.views import MessagesInboxView, MessageThreadView, SendMessageView


urlpatterns = [
    path("inbox/", MessagesInboxView.as_view()),
    path("thread/<receiver_id>/", MessageThreadView.as_view()),
    path("send/", SendMessageView.as_view()),
]
