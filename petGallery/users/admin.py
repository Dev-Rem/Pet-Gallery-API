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
    list_display = ("user", "question", "created_at", "last_used")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "animal", "gender", "breed")


@admin.register(CustomUser)
class CustomeUserAdmin(admin.ModelAdmin):
    list_display = ("username", "date_joined", "last_login", "is_active", "is_staff")


@admin.register(FollowAccount)
class AccountFollowingAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "created")


@admin.register(BlockAccount)
class AccountBlockedAdmin(admin.ModelAdmin):
    list_display = ("user", "created")
