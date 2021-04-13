from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views

router = DefaultRouter()
router.register('list', views.AllOrderViewSet, basename='all-order-list')
router.register('create', views.CreateOrderViewSet, basename='order-list')
router.register('execute', views.ExecuteOrderView, basename='change-executor')
router.register('decline', views.DeclineValidOrderViewSet, basename='decline-order-data')
router.register('not_valid_list', views.NotValidOrderViewSet, basename='not-valid-order-list')
router.register('reviews', views.ReviewView, basename='review-list')
router.register('review-images', views.ReviewImagesView, basename='review-images')
router.register('review-scans', views.ReviewScansView, basename='review-scans')
router.register('review-accept', views.AcceptReviewOrderView, basename='accept-review')
router.register('review-decline', views.DeclineReviewOrderView, basename='decline-review')


urlpatterns = [
    path('', include(router.urls)),
]