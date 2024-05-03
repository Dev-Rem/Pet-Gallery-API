from django.urls import path

from petGallery.posts.views.views1 import PostView, ArchivePostView, SavePostView


urlpatterns = [
    path("posts/", PostView.as_view()),
    path("posts/archive/", ArchivePostView.as_view()),
    path("posts/save/", SavePostView.as_view()),
]
