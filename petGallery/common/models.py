from django.db import models


# Create your models here.
class AbstractBaseModel(models.Model):
    """
    Base abstract model, that includes
    `created_at` and `updated_at` fields.
    """

    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        abstract = True
