from django.urls import path

from posts.views.views1 import PostView, ArchivePostView, SavePostView
from posts.views.views2 import (
    FeedPostsView,
    ExplorePostsView,
    TaggedPostsView,
    LikePostsView,
)


urlpatterns = [
    path("posts/", PostView.as_view()),
    path("posts/archive/", ArchivePostView.as_view()),
    path("posts/save/", SavePostView.as_view()),
    path("posts/feed/", FeedPostsView.as_view()),
    path("posts/explore/", ExplorePostsView.as_view()),
    path("posts/tagged/", TaggedPostsView.as_view()),
    path("posts/like/", LikePostsView.as_view()),
]
