from users.views import (
    UserRegisterView,
    AccountInfoView,
    AccountUpdateView,
    AccountListView,
    ChangePasswordView,
    CreateSecurityQuestionView,
    ResetPasswordView,
    FollowAccountView,
    BlockAccountView,
    FollowRequestView,
)
from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("users/register/", UserRegisterView.as_view()),
    path("users/change-password/", ChangePasswordView.as_view()),
    path("users/reset-password/", ResetPasswordView.as_view()),
    path("users/account/", AccountListView.as_view()),
    path("users/account/info/", AccountInfoView.as_view()),
    path("users/account/update/", AccountUpdateView.as_view()),
    path("users/account/security-question/", CreateSecurityQuestionView.as_view()),
    path("users/account/follow/", FollowAccountView.as_view()),
    path("users/account/block/", BlockAccountView.as_view()),
    path("users/account/request/", FollowRequestView.as_view()),
]
