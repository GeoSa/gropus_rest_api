from rest_framework import serializers
from .models import Passport


class PassportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passport
        fields = '__all__'
