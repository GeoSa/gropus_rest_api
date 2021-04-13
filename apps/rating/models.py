from django.db import models
from ..user.models import ExecutorProfile


class Rating(models.Model):
    orders = models.IntegerField(default=0)
    closed_orders = models.IntegerField(default=0)
    user = models.ForeignKey(ExecutorProfile, on_delete=models.CASCADE, related_name='rating')

    def __str__(self):
        return f'{self.user}'
