from django.db import models
from apps.region.models import Region, City
from apps.user.models import User


class Order(models.Model):

    customer_number = models.CharField(max_length=20, blank=True)
    customer_address = models.CharField(max_length=150, blank=True)
    customer = models.CharField(max_length=150, blank=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, blank=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, related_name='created_by', null=True)

    order_type = models.SmallIntegerField(default=2)     # 1 - free or 2 - payable
    valid = models.BooleanField(default=True)      # validation order info by executor
    paid_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    paid_status = models.SmallIntegerField(default=2)   # 1 - paid or 2 - not paid
    order_amount = models.IntegerField(null=True)
    start_time = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    moderation_time = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    approve_status = models.SmallIntegerField(default=2)  # 1 - approved, 2 - not approved
    approve_time = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    rp_approve_time = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    repeat_moderation_time = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    repeat_approve_time = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    # source of order (1 - site, 3 - executor, 4 - rp, 2 - customer)
    order_source = models.SmallIntegerField(blank=True, default=2)  # 1 - site, 2 - platform
    paid_order_amount = models.IntegerField(null=True)
    # order status 1 - create, 2 - execute, 3 - approve, 4 - closed
    status = models.SmallIntegerField('Order status', default=1)
    rp = models.ForeignKey(User, related_name='order_rp', on_delete=models.DO_NOTHING, null=True, blank=True)
    executor = models.ForeignKey(User, related_name='order_executor', on_delete=models.DO_NOTHING, null=True, blank=True)
    archive = models.BooleanField(default=False)        # displayed old orders in archive
    payments = models.BooleanField(default=False)

    def __str__(self):
        return f'${self.id}'

    def description(self):
        return f"description"


class Review(models.Model):

    description = models.CharField(max_length=255)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='review', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f'${self.pk}'


class ReviewImages(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to='review/images')


class ReviewScans(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='scans')
    scans = models.ImageField(upload_to='review/scans')
