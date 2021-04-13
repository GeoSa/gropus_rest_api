from django.db import models
from ..order.models import Order
from ..user.models import User


class Notification(models.Model):

    # status: 1 - read, 2 - not read
    status = models.SmallIntegerField(default=2)
    # types: 1 - for customer, 2 - for executor, 3 - for regional representative
    type = models.SmallIntegerField()
    description = models.CharField(max_length=255, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, related_name='notification')

    def __str__(self):
        return f'{self.description}'
