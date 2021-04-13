from django.db import models
from ..user.models import User


class Passport(models.Model):

    face_photo = models.ImageField(upload_to='passport_data/')
    passport_photo = models.ImageField(upload_to='passport_data/')
    adr_photo = models.ImageField(upload_to='passport_data/')
    passport_data = models.CharField(unique=True, max_length=16)
    issued_by = models.CharField(max_length=100)
    when_issued = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passport')

    def __str__(self):
        return f'{self.passport_data}'
