from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views


router = DefaultRouter()
router.register('region', views.RegionView, basename='region-list')
router.register('city', views.CityView, basename='city-list')

urlpatterns = [
    path('', include(router.urls)),
]