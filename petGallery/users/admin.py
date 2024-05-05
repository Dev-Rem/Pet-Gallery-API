from django.contrib import admin
from users.models import (
    Account,
    CustomUser,
    SecurityQuestion,
    FollowAccount,
    BlockAccount,
    FollowRequest,
)

# Register your models here.


@admin.register(SecurityQuestion)
class SecurityQuestionAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "created_at", "updated_at")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "animal",
        "gender",
        "breed",
        "created_at",
        "updated_at",
    )


@admin.register(CustomUser)
class CustomeUserAdmin(admin.ModelAdmin):
    list_display = ("username", "date_joined", "last_login", "is_active", "is_staff")


@admin.register(FollowAccount)
class FollowAccountAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "created_at", "updated_at")


@admin.register(BlockAccount)
class BlockAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")


@admin.register(FollowRequest)
class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ("request_from", "request_to", "status", "created_at", "updated_at")
