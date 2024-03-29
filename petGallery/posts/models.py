from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(_("Date Created"), auto_now_add=True)



class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    caption = models.TextField(_("Caption"), max_length=5000, null=True)
    location = models.CharField(_("Location"), null=True, blank=True, max_length=255)
    is_deleted = models.BooleanField(_("Is Deleted"), default=False)
    likes = models.ManyToManyField(
        CustomUser, related_name="liked_posts", blank=True, verbose_name=_("Liked By")
    )
    hashtags = models.ManyToManyField(
        Hashtag, related_name="posts", blank=True, verbose_name=_("Hashtags")
    )
    date_posted = models.DateTimeField(_("Date Posted"), auto_now_add=True)

    class Meta:
        ordering = ["-date_posted"]


class SavedPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    posts = models.ManyToManyField(
        Post, related_name="saved_by", verbose_name=_("Posts Saved"), blank=True
    )
    saved_at = models.DateTimeField(_("Date Saved"), auto_now_add=True)


class ArchivedPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="archived_by")
    archived_at = models.DateTimeField(_("Date Archived"), auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")


class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    text = models.TextField(_("Comment"), null=True)
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
    comment_date = models.DateTimeField(_("Date Commented"), auto_now_add=True)


class Image(models.Model):
    post = models.ForeignKey(
        Post, null=True, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(_("Image"), upload_to="post_images/", null=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
