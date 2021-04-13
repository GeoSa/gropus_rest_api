from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from .models import Order, Review, ReviewImages, ReviewScans
from .serializers import (
    FullOrderSerializer,
    OrderSerializer,
    DeclineValidOrderSerializer,
    ExecutorTakeOrderSerializer,
    ReviewSerializer,
    AcceptReviewSerializer,
    DeclineReviewSerializer,
    ReviewImagesSerializer,
    ReviewScansSerializer
)
from .utils import get_order_amount
from ..user.permission import IsRpOrExecutorUser, AllUser, IsRpUser


class AllOrderViewSet(ModelViewSet):

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        approve = self.request.query_params.get('approve', None)
        if status is None and approve is None:
            queryset = Order.objects.filter(region=self.request.user.region, archive=False,)
        elif status is not None and approve is None:
            queryset = Order.objects.filter(region=self.request.user.region, archive=False, status=status)
        else:
            queryset = Order.objects.filter(region=self.request.user.region, archive=False, status=status, approve_status=approve)

        return queryset

    serializer_class = FullOrderSerializer
    http_method_names = ['get']
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = [AllUser]
        return [permission() for permission in permission_classes]


class CreateOrderViewSet(ModelViewSet):

    def get_queryset(self):
        return Order.objects.filter(region=self.request.user.region, archive=False)

    serializer_class = OrderSerializer
    http_method_names = ['put', 'post', 'get']
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

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


class NotValidOrderViewSet(ModelViewSet):

    def get_queryset(self):
        return Order.objects.filter(
            region=self.request.user.region,
            archive=False,
            valid=False,
            customer=self.request.user,
            status=2,
        )

    serializer_class = OrderSerializer
    http_method_names = ['get', 'put', 'patch']
    authentication_classes = [TokenAuthentication]

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = [AllUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [AllUser]
        return [permission() for permission in permission_classes]


class DeclineValidOrderViewSet(ModelViewSet):

    def get_queryset(self):
        return Order.objects.filter(
            archive=False,
            executor=self.request.user,
            region=self.request.user.region,
            status=2
        )
    serializer_class = DeclineValidOrderSerializer
    http_method_names = ['put']
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsRpOrExecutorUser]
        return [permission() for permission in permission_classes]


class ExecuteOrderView(ModelViewSet):

    queryset = Order.objects.filter(archive=False, executor=None)
    serializer_class = ExecutorTakeOrderSerializer
    http_method_names = ['put', 'get']
    authentication_classes = [TokenAuthentication]

    def perform_update(self, serializer):
        serializer.save(executor=self.request.user)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = [IsRpOrExecutorUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsRpOrExecutorUser]
        return [permission() for permission in permission_classes]


class ReviewView(ModelViewSet):
    def get_queryset(self,):
        order = self.request.query_params.get('order', None)
        if order is not None:
            return Review.objects.filter(user=self.request.user, order=order)

    serializer_class = ReviewSerializer
    http_method_names = ['put', 'post', 'get']
    authentication_classes = [TokenAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsRpOrExecutorUser]
        elif self.action == 'list':
            permission_classes = [IsRpOrExecutorUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsRpOrExecutorUser]
        elif self.action == 'destroy':
            permission_classes = [IsRpOrExecutorUser]
        return [permission() for permission in permission_classes]


class AcceptReviewOrderView(ModelViewSet):

    def get_queryset(self):
        return Order.objects.filter(archive=False, rp=self.request.user, status=3, approve_status=2)

    serializer_class = AcceptReviewSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ['put', 'get']

    def get_permissions(self):
        permission_classes = []
        if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsRpUser]
        return [permission() for permission in permission_classes]


class DeclineReviewOrderView(ModelViewSet):

    def get_queryset(self):
        return Order.objects.filter(archive=False, rp=self.request.user, status=3, approve_status=2)
    serializer_class = DeclineReviewSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ['put', 'get']

    def get_permissions(self):
        permission_classes = []
        if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsRpUser]
        return [permission() for permission in permission_classes]


class ReviewImagesView(ModelViewSet):

    def get_queryset(self):
        review = self.request.query_params.get('review', None)
        if review is not None:
            return ReviewImages.objects.filter(review=review)

    serializer_class = ReviewImagesSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsRpOrExecutorUser]
        elif self.action == 'list':
            permission_classes = [IsRpOrExecutorUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsRpOrExecutorUser]
        elif self.action == 'destroy':
            permission_classes = [IsRpOrExecutorUser]
        return [permission() for permission in permission_classes]


class ReviewScansView(ModelViewSet):

    def get_queryset(self):
        review = self.request.query_params.get('review', None)
        if review is not None:
            return ReviewScans.objects.filter(review=review)

    serializer_class = ReviewScansSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsRpOrExecutorUser]
        elif self.action == 'list':
            permission_classes = [IsRpOrExecutorUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsRpOrExecutorUser]
        elif self.action == 'destroy':
            permission_classes = [IsRpOrExecutorUser]
        return [permission() for permission in permission_classes]
