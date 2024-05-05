from django.contrib import admin
from posts.models import Hashtag, Post, Comment, Image, SavePost, ArchivePost

# Register your models here.


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "location",
        "created_at",
        "updated_at",
        "is_deleted",
        "is_archived",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "text", "created_at", "updated_at")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("post", "image", "created_at", "updated_at")


@admin.register(SavePost)
class SavePostAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")


@admin.register(ArchivePost)
class ArchivePostAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at", "updated_at")
