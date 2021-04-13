from rest_framework import serializers
from .models import Region, City


class CitySerializer(serializers.ModelSerializer):
    #region = RegionSerializer

    class Meta:
        model = City
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):

    cities = CitySerializer

    class Meta:
        model = Region
        fields = "__all__"
