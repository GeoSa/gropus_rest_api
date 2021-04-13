from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from .serializers import PassportSerializer
from .models import Passport


class PassportView(ModelViewSet):

    def get_queryset(self):
        return Passport.objects.filter(user=self.request.user)

    serializer_class = PassportSerializer
    authentication_classes = [TokenAuthentication]
