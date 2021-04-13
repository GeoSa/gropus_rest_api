from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from .models import Notification
from .serializer import NotificationSerializer
from ..user.permission import AllUser


class NotificationView(ModelViewSet):

    def get_queryset(self):
        order = self.request.query_params.get('pk', None)
        group = None
        if str(self.request.user.groups) == 'customer':
            group = 1
        elif str(self.request.user.groups) == 'executor':
            group = 2
        elif str(self.request.user.groups) == 'regional representative':
            group = 3

        if order is not None:
            return Notification.objects.filter(order=order, type=group, status=2)
        else:
            return Notification.objects.filter(type=group, status=2)

    serializer_class = NotificationSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllUser]
        elif self.action == 'list':
            permission_classes = [AllUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [AllUser]
        elif self.action == 'destroy':
            permission_classes = [AllUser]
        return [permission() for permission in permission_classes]
