from users.views import UserRegistrationView
from django.urls import path

urlpatterns = [
    path("accounts/registration/", UserRegistrationView.as_view()),
]
