from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views

router = DefaultRouter()
router.register('admin', views.AdminViewSet, basename='admin-list')
router.register('rp', views.RpViewSet, basename='rp-list')
router.register('executor', views.ExecutorViewSet, basename='executor-list')
router.register('customer', views.CustomerViewSet, basename='customer-list')
router.register('lock-rp', views.LockRPViewSet, basename='lock-rp-list')
router.register('lock-executor', views.LockExecutorViewSet, basename='lock-exec-list')
router.register('login', views.LoginView, basename='login')
router.register('password', views.ChangePasswordView, basename='password-list')

urlpatterns = [
    path('', include(router.urls)),
    path('account/logout/', views.LogoutView.as_view(), name='logout'),
]
