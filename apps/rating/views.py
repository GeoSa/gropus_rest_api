from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import RatingSerializer
from .models import Rating
from ..user.models import ExecutorProfile


class RatingView(ModelViewSet):
    def get_queryset(self):
        if ExecutorProfile.objects.all().filter(user=self.request.user).exists():
            return Rating.objects.filter(user=ExecutorProfile.objects.get(user=self.request.user))

    serializer_class = RatingSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ['get']
