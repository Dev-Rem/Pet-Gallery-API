from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime, date
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from common.models import AbstractBaseModel


GENDER_CHOICES = (("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other"))
ANIMALS = (("DOG", "Dog"), ("CAT", "Cat"), ("PARROT", "Parrot"), ("OTHER", "Other"))
SECURITY_QUESTIONS = (
    ("favorite_toy", "What is your pet's favorite toy?"),
    ("favorite_treat", "What is your pet's favorite treat?"),
    ("best_friend", "What is the name of your pet's best friend?"),
    ("collar_color", "What is the color of your pet's collar?"),
    ("favorite_place_to_sleep", "What is your pet's favorite place to sleep?"),
    ("favorite_activity", "What is your pet's favorite activity?"),
    ("veterinarian_name", "What is the name of your pet's veterinarian?"),
    ("favorite_food", "What is your pet's favorite food?"),
    ("breed", "What is the breed of your pet?"),
    ("birth_month", "What is your pet's birth month?"),
    ("favorite_game_to_play", "What is your pet's favorite game to play?"),
    ("nickname", "What is your pet's nickname?"),
)
FOLLOW_REQUEST_STATUS = (
    ("ACCEPTED", "Accepted"),
    ("DECLINED", "Declined"),
    ("PENDING", "Pending"),
    ("CANCELLED", "Cancelled"),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("The Username field must be set")

        user = self.model(username=username)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):

        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    date_joined = models.DateField(
        _("Date Joined"), auto_now=False, default=datetime.now
    )
    last_login = models.DateTimeField(_("Date Last log in"), default=datetime.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username


class Account(AbstractBaseModel):
    name = models.CharField(_("Name"), max_length=150)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.CharField(_("Bio"))
    age = models.IntegerField(_("Age"))
    gender = models.CharField(_("Gender"), max_length=20, choices=GENDER_CHOICES)
    animal = models.CharField(_("Animal"), max_length=50, choices=ANIMALS)
    breed = models.CharField(_("Breed"), max_length=50)
    private = models.BooleanField(_("Private account"), default=False)
    verified = models.BooleanField(_("Verified account"), default=False)
    avatar = models.ImageField(
        _("Profile photo"), upload_to="profile_photos", default="default.png"
    )

    def __str__(self):
        return self.name


class FollowAccount(AbstractBaseModel):

    follower = models.ForeignKey(
        Account, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        Account, related_name="followers", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower_id", "following_id"],
                name="unique_followers",
            )
        ]
        ordering = ["-created_at"]


class BlockAccount(AbstractBaseModel):
    user = models.ForeignKey(
        Account, related_name="blocked_users", on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        Account, verbose_name=_("Blocked Users"), related_name="blocked_by"
    )


class FollowRequest(AbstractBaseModel):
    request_from = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="sent_follow_requests",
        verbose_name=_("From Account"),
    )
    request_to = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="received_follow_requests",
        verbose_name=_("To Account"),
    )
    status = models.CharField(
        _("Request status"), choices=FOLLOW_REQUEST_STATUS, default="PENDING"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["request_from", "request_to"], name="unique_follow_request"
            )
        ]


class SecurityQuestion(AbstractBaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    question = models.CharField(
        _("Question"), max_length=150, choices=SECURITY_QUESTIONS
    )
    answer = models.CharField(_("Answer"), max_length=150)
