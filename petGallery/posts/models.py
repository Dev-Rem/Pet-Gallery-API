from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from common.models import AbstractBaseModel


class Hashtag(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)


class Post(AbstractBaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    caption = models.TextField(_("Caption"), max_length=5000, null=True, blank=True)
    location = models.CharField(_("Location"), blank=True, null=True, max_length=255)
    is_deleted = models.BooleanField(_("Is Deleted"), default=False)
    is_archived = models.BooleanField(_("Is Archived"), default=False)

    likes = models.ManyToManyField(
        CustomUser, related_name="liked_posts", blank=True, verbose_name=_("Liked By")
    )
    tags = models.ManyToManyField(
        CustomUser,
        related_name="tagged_users",
        blank=True,
        verbose_name=_("Tagged Users"),
    )
    hashtags = models.ManyToManyField(
        Hashtag, related_name="posts", blank=True, verbose_name=_("Hashtags")
    )

    class Meta:
        ordering = ["-created_at"]


class Image(AbstractBaseModel):
    post = models.ForeignKey(
        Post, null=True, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(_("Image"), upload_to="post_images/")


class SavePost(AbstractBaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    posts = models.ManyToManyField(
        Post, related_name="saved_by", verbose_name=_("Posts Saved"), blank=True
    )
    created = models.DateField(
        verbose_name="Date Added", auto_now=False, auto_now_add=True
    )
    updated = models.DateTimeField(verbose_name="Date Last Updated", auto_now=True)

    class Meta:
        ordering = ["-created_at"]


class ArchivePost(AbstractBaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="archived_by")

    class Meta:
        unique_together = ("user", "post")
        ordering = ["-created_at"]


class Comment(AbstractBaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(
        _("Comment"),
    )
    replies = models.ForeignKey(
        "self",
        blank=True,
        related_name="comment_replies",
        on_delete=models.CASCADE,
        null=True,
    )
    is_deleted = models.BooleanField(_("Is Deleted"), default=False)
    likes = models.ManyToManyField(
        CustomUser,
        related_name="liked_comments",
        verbose_name=_("Liked By"),
    )
    edited = models.BooleanField(_("Edited Comment"), default=False)

    class Meta:
        ordering = ["-created_at"]
