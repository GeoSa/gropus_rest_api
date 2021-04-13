from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from ..region.models import Region
from rest_framework.validators import UniqueValidator


class User(AbstractUser):
    # Groups: 1 - admin. 2 - regional representative, 3 - executor, 4 - customer
    groups = models.ForeignKey(Group, on_delete=models.DO_NOTHING, blank=True)
    email = models.EmailField(max_length=50, unique=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, related_name='user', null=True)
    username = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, blank=True, unique=True)
    first_password = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['groups_id', 'username']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.pk}'


class AdminProfile(models.Model):

    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='admin_profile',
        blank=True
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    second_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.pk}'


class RPProfile(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='rp_profile',
        blank=True
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    second_name = models.CharField(max_length=50, blank=True)
    zam = models.ForeignKey(User, related_name='zam', on_delete=models.DO_NOTHING, null=True)
    first_rp = models.BooleanField(default=False)
    status = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'{self.pk}'


class ExecutorProfile(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='executor_profile',
        blank=True
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    second_name = models.CharField(max_length=50, blank=True)
    rp = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, related_name='reg_rep', null=True)
    status = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'{self.pk}'


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        blank=True
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    second_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.pk}'
