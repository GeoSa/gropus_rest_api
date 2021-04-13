from rest_framework import serializers
from ..user.serializers import UserSerializer
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ['balance', 'last_balance',]
        # exclude = ('id',)
