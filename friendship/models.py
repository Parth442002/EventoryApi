from turtle import mode
from django.contrib.gis.db import models
import uuid
from authentication.models import Account
# Create your models here.


class FriendRequest(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    from_account = models.ForeignKey(
        Account, verbose_name="from_account", on_delete=models.CASCADE)
    to_account = models.ForeignKey(
        Account, verbose_name="to_account", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    send_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.from_account.primary_identifier+"# to "+self.to_account.primary_identifier
