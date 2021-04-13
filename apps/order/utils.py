from datetime import datetime
from .models import Order
from .payments import payments
from apps.region.models import Region
from apps.user.models import User
from apps.notification.models import Notification


def get_order_amount(validated_data):

    region = Region.objects.get(pk=validated_data['region'].id)
    creator = User.objects.get(pk=validated_data['created_by'].id)

    if 'order_type' not in validated_data:
        pass
    elif validated_data['order_type'] == 1:
        return None

    if validated_data['order_source'] == 1:
        costs = region.order_site_price
    else:
        if str(creator.groups) == 'customer':
            costs = region.order_customer_price
        else:
            costs = region.order_executor_price

    return costs


def update_order(validated_data):
    order = Order.objects.get(pk=validated_data['order'].id)
    order.approve_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    order.approve_status = 2

    if order.status != 4:
        if order.rp == order.executor:
            order.status = 4
            order.approve_status = 1
            order.rp_approve_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            payments(order.pk)
        else:
            order.status = 3
            create_notification(3, validated_data['description'], validated_data['order'])
    else:
        if order.rp == order.executor:
            order.rp_approve_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            order.approve_status = 1
        else:
            order.repeat_approve_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            create_notification(3, validated_data['description'], validated_data['order'])

    order.save()


def create_notification(tp, description, order):
    Notification.objects.create(
        status=2,
        type=tp,
        description=description,
        order=order
    )
