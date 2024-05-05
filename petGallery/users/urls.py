from users.views.views1 import (
    UserRegisterView,
    AccountInfoView,
    AccountUpdateView,
    AccountListView,
    ChangePasswordView,
    CreateSecurityQuestionView,
    ResetPasswordView,
    FollowAccountView,
)
from users.views.views2 import (
    BlockAccountView,
    FollowRequestView,
    FollowRequestSentView,
)
from django.urls import path

urlpatterns = [
    path("register/", UserRegisterView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
    path("account/", AccountListView.as_view()),
    path("account/info/", AccountInfoView.as_view()),
    path("account/update/", AccountUpdateView.as_view()),
    path("account/security-question/", CreateSecurityQuestionView.as_view()),
    path("account/follow/", FollowAccountView.as_view()),
    path("account/block/", BlockAccountView.as_view()),
    path("account/request/", FollowRequestView.as_view()),
    path("account/sent-request/", FollowRequestSentView.as_view()),
]
