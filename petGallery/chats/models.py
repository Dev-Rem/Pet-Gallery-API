from django.db import models
from users.models import CustomUser, Account
from common.models import AbstractBaseModel
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Chat(AbstractBaseModel):
    class Meta:
        ordering = ["-created_at"]

    sender = models.ForeignKey(
        CustomUser, related_name="sender", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        CustomUser, related_name="receiver", on_delete=models.CASCADE
    )
    is_read = models.BooleanField(_("Read Message"), default=False)
    is_edited = models.BooleanField(_("Edited Message"), default=False)
    message = models.TextField("Message text")
    conversation_code = models.CharField(max_length=50)

    @property
    def sender_account(self):
        sender_account = Account.objects.get(user=self.sender)
        return sender_account

    @property
    def receiver_account(self):
        receiver_account = Account.objects.get(user=self.receiver)
        return receiver_account
