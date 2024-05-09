from django.urls import path

from chats.views import MessagesInbox


urlpatterns = [
    path("inbox/", MessagesInbox.as_view()),
]
