from django.urls import path

from posts.views import PostView, ArchivePostView


urlpatterns = [
    path("posts/", PostView.as_view()),
    path("posts/archive/", ArchivePostView.as_view()),
]
