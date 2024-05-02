from django.urls import path

from posts.views import PostCreateView, ArchivePostView


urlpatterns = [
    path("posts/create/", PostCreateView.as_view()),
    path("posts/archive/", ArchivePostView.as_view()),
]
