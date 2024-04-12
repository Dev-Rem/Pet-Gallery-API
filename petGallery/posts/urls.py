from django.urls import path

from posts.views import PostCreateView


urlpatterns = [
    path("posts/create/", PostCreateView.as_view()),
]
