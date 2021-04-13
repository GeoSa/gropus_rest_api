import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from apps.order.models import Order
from datetime import timedelta, datetime

delta = timedelta(days=30)
now = datetime.today()
delta_time = now - delta


def handler():
    orders = Order.objects.filter(update_time__lte=delta_time, archive=False, status=4)

    for order in orders:
        order.archive = True
        order.save()


if __name__ == '__main__':
    handler()
