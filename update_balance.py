import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from apps.wallet.models import Wallet


def handler():

    wallets = Wallet.objects.all()

    for wallet in wallets:
        wallet.last_balance = wallet.balance
        wallet.balance = 0
        wallet.save()


if __name__ == '__main__':
    handler()
