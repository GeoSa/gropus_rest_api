from apps.user.models import User, RPProfile
from apps.wallet.models import Wallet
from apps.order.models import Order


def payments(instance):

    order = Order.objects.get(pk=instance)
    region_data = order.region
    executor = order.executor.id
    rp = order.rp.id
    first_rp = RPProfile.objects.get(user__region=order.region, first_rp=True)
    first_rp = User.objects.get(pk=first_rp.pk)

    system_balance = 0
    executor_balance = 0
    rp_balance = 0
    first_rp_balance = 0

    if order.order_source == 1 and order.order_type == 2:
        executor_balance = region_data.executor_rate_site
        rp_balance = region_data.rate_rp_site
        first_rp_balance = region_data.rate_first_rp_site
        system_balance = region_data.commission_site
    elif order.order_type == 2:
        if str(order.created_by.groups) == 'customer':
            executor_balance = region_data.executor_rate_customer
            rp_balance = region_data.rate_rp_customer
            first_rp_balance = region_data.rate_first_rp_customer
            system_balance = region_data.commission_customer
        else:
            executor_balance = region_data.executor_rate_executor
            rp_balance = region_data.rate_rp_executor
            system_balance = region_data.commission_executor

    execute_payments(executor, executor_balance)
    execute_payments(rp, rp_balance)
    execute_payments(first_rp, first_rp_balance)
    execute_payments(1, system_balance)

    order.payments = True
    order.save()


def execute_payments(user, payment):
    wallet = Wallet.objects.get(user=user)
    cur_balance = wallet.balance + payment
    Wallet.objects.filter(user=user).update(balance=cur_balance)


