from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from .permission import IsAdminUser, IsAdminOrRpUser, IsRpOrExecutorUser, AllUser
from .models import User, AdminProfile, RPProfile, ExecutorProfile, CustomerProfile
from .serializers import (
    AdminSerializer,
    RPSerializer,
    ExecutorSerializer,
    CustomerSerializer,
    LockRPSerializer,
    LockExecutorSerializer,
    ChangePasswordSerializer
)


class LockRPViewSet(ModelViewSet):
    def get_queryset(self):
        return RPProfile.objects.filter(user__region=self.request.user.region)

    serializer_class = LockRPSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ('get', 'put',)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class LockExecutorViewSet(ModelViewSet):
    def get_queryset(self):
        return ExecutorProfile.objects.filter(rp=self.request.user)

    serializer_class = LockExecutorSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ('get', 'put',)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = [IsAdminOrRpUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminOrRpUser]
        return [permission() for permission in permission_classes]


class AdminViewSet(ModelViewSet):

    def get_queryset(self):
        queryset = AdminProfile.objects.filter(user=self.request.user)
        return queryset
    serializer_class = AdminSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class RpViewSet(ModelViewSet):

    def get_queryset(self):
        if str(self.request.user.groups) == 'regional representative':
            return RPProfile.objects.filter(user=self.request.user)
        elif str(self.request.user.groups) == 'admin':
            return RPProfile.objects.filter(user__region=self.request.user.region)

    serializer_class = RPSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'list':
            permission_classes = [IsAdminOrRpUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminOrRpUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ExecutorViewSet(ModelViewSet):

    def get_queryset(self):
        if str(self.request.user.groups) == 'executor':
            return ExecutorProfile.objects.filter(user=self.request.user)
        elif str(self.request.user.groups) == 'regional representative':
            return ExecutorProfile.objects.filter(rp=self.request.user)
        elif str(self.request.user.groups) == 'admin':
            return ExecutorProfile.objects.all()

    serializer_class = ExecutorSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(rp=self.request.user)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminOrRpUser]
        elif self.action == 'list':
            permission_classes = [IsRpOrExecutorUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsRpOrExecutorUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminOrRpUser]
        return [permission() for permission in permission_classes]


class CustomerViewSet(ModelViewSet):

    def get_queryset(self):
        if str(self.request.user.groups) == 'customer':
            return CustomerProfile.objects.filter(user=self.request.user)
        else:
            return CustomerProfile.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication]


class LoginView(ViewSet):
    serializer_class = AuthTokenSerializer

    @staticmethod
    def create(request):
        return ObtainAuthToken().post(request)


class LogoutView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ChangePasswordView(ModelViewSet):

    def get_queryset(self):
        return User.objects.filter(email=self.request.user.email)

    serializer_class = ChangePasswordSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ['get', 'put']
