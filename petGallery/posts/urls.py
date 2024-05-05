from django.urls import path

from posts.views.views1 import PostView, ArchivePostView, SavePostView
from posts.views.views2 import (
    FeedPostsView,
    ExplorePostsView,
    TaggedPostsView,
    LikePostsView,
    CommentsView,
)


urlpatterns = [
    path("", PostView.as_view()),
    path("archive/", ArchivePostView.as_view()),
    path("save/", SavePostView.as_view()),
    path("feed/", FeedPostsView.as_view()),
    path("explore/", ExplorePostsView.as_view()),
    path("tagged/", TaggedPostsView.as_view()),
    path("like/", LikePostsView.as_view()),
    path("comments/", CommentsView.as_view()),
]
