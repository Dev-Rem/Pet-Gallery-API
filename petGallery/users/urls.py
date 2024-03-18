from users.views import UserRegisterView
from django.urls import path

urlpatterns = [
    path("users/register/", UserRegisterView.as_view()),
]
