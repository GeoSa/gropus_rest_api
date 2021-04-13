from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from .serializers import WalletSerializer
from .models import Wallet


class WalletView(ModelViewSet):
    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)
    serializer_class = WalletSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
