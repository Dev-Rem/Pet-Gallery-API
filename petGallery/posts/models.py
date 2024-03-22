from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    caption = models.TextField(_("Caption"), max_length=5000, null=True)
    is_archived = models.BooleanField(_("Is Archived"), default=False)
    is_deleted = models.BooleanField(_("Is Deleted"), default=False)
    liked_by = models.ManyToManyField(
        CustomUser, related_name="liked_posts", blank=True, verbose_name=_("Liked By")
    )
    date = models.DateTimeField(_("Date"), auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    comment = models.TextField(_("Comment"), null=True)
    reply = models.ForeignKey(
        "self", null=True, related_name="replies", on_delete=models.CASCADE
    )
    is_deleted = models.BooleanField(_("Is Deleted"), default=False)
    liked_by = models.ManyToManyField(
        CustomUser,
        related_name="liked_comments",
        blank=True,
        verbose_name=_("Liked By"),
    )
    date = models.DateTimeField(_("Date"), auto_now_add=True)


class Image(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to="post_images/", null=True)
    date = models.DateTimeField(_("Date"))
