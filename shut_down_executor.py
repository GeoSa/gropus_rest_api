import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from datetime import timedelta, datetime
from apps.order.models import Order


delta = timedelta(days=10)
now = datetime.today()
delta_time = now - delta


def handler():

    orders = Order.objects.filter(start_time_lte=delta_time, status=2)

    for order in orders:
        if not order.approve_time:
            order.executor = None
            order.rp = None
            order.start_time = None
            order.valid = True
            order.status = 1
            order.save()
        else:
            continue


if __name__ == '__main__':
    handler()
