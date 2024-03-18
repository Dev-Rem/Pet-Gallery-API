from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password


GENDER_CHOICES = (("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other"))
ANIMALS = (("DOG", "Dog"), ("CAT", "Cat"), ("PARROT", "Parrot"), ("OTHER", "Other"))


class Account(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    username = models.CharField(_("Username"), max_length=20, unique=True)
    bio = models.CharField(_("Bio"), blank=True)
    age = models.IntegerField(_("Age"))
    gender = models.CharField(_("Gender"), max_length=20, choices=GENDER_CHOICES)
    animal = models.CharField(_("Animal"), max_length=50, choices=ANIMALS)
    breed = models.CharField(_("Breed"), max_length=50)
    password = models.CharField(_("Password"), max_length=100)
    date_joined = models.DateField(
        _("Date Joined"), auto_now=False, default=datetime.now
    )
    last_login = models.DateTimeField(_("Date Last log in"), default=datetime.now)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
