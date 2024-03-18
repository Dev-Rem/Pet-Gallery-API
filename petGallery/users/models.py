from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


GENDER_CHOICES = (("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other"))
ANIMALS = (("DOG", "Dog"), ("CAT", "Cat"), ("PARROT", "Parrot"), ("OTHER", "Other"))


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
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username


class Account(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.CharField(_("Bio"))
    age = models.IntegerField(_("Age"))
    gender = models.CharField(_("Gender"), max_length=20, choices=GENDER_CHOICES)
    animal = models.CharField(_("Animal"), max_length=50, choices=ANIMALS)
    breed = models.CharField(_("Breed"), max_length=50)
    date_joined = models.DateField(
        _("Date Joined"), auto_now=False, default=datetime.now
    )
    last_login = models.DateTimeField(_("Date Last log in"), default=datetime.now)

    def __str__(self):
        return self.name
