from django.contrib import admin
from chats.models import Chat

# Register your models here.


@admin.register(Chat)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "sender",
        "receiver",
        "message",
        "is_edited",
        "conversation_code",
        "created_at",
        "updated_at",
    )
