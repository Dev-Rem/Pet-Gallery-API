from django.contrib import admin
from posts.models import Hashtag, Post, Comment, Image, SavedPost

# Register your models here.


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "date_posted", "is_deleted")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "text", "comment_date")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("post", "image")


@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ("user", "saved_at")
