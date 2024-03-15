from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

GENDER_CHOICES = (("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other"))


class CustomUser(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(_("Name"), max_length=150, unique=True)
    pet_code = models.CharField(_("Pet Code"), max_length=10, unique=True)
    age = models.IntegerField(_("Age"))
    gender = models.CharField(_("Gender"), max_length=20, choices=GENDER_CHOICES)
    animal = models.CharField(_("Animal"), max_length=50)
    breed = models.CharField(_("Breed"), max_length=50)

    # Define the field to use as the unique identifier for the user
    USERNAME_FIELD = "pet_code"

    # Define the required fields for creating a user
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name
