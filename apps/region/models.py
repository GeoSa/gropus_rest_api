from django.db import models


class Region(models.Model):

    name = models.CharField("Region", max_length=100)
    order_site_price = models.IntegerField()
    order_rp_price = models.IntegerField()
    order_customer_price = models.IntegerField()
    order_executor_price = models.IntegerField()
    rate_rp_customer = models.IntegerField()
    rate_rp_executor = models.IntegerField()
    rate_rp_site = models.IntegerField()
    rate_first_rp_site = models.IntegerField()
    rate_first_rp_customer = models.IntegerField()
    executor_rate_site = models.IntegerField()
    executor_rate_customer = models.IntegerField()
    executor_rate_executor = models.IntegerField()
    commission_site = models.IntegerField()
    commission_customer = models.IntegerField()
    commission_executor = models.IntegerField()

    class Meta:
        verbose_name = 'region'
        verbose_name_plural = 'regions'

    def __str__(self):
        return self.name


class City(models.Model):

    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, verbose_name="Region", related_name="region", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name
