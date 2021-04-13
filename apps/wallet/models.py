from django.db import models
from ..user.models import User


class Wallet(models.Model):

    balance = models.IntegerField(default=0)
    last_balance = models.IntegerField(default=0)
    name_receiver = models.CharField(max_length=50, null=True)
    calc_account = models.CharField(max_length=100, unique=True, null=True)
    corr_account = models.CharField(max_length=100, unique=True, null=True)
    bank_name = models.CharField(max_length=50, null=True)
    bik = models.CharField(max_length=50, unique=True, null=True)
    inn = models.CharField(max_length=50, unique=True, null=True)
    bank_code = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')

    def __str__(self):
        return f"{self.name_receiver}"
