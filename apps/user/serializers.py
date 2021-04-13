from django.core.validators import EmailValidator
from rest_framework import serializers
from .models import User, AdminProfile, RPProfile, ExecutorProfile, CustomerProfile, Group
from .user_utils import create_user, update_user, change_lock_rp, reset_executor
from ..rating.serializers import RatingSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('pk', 'email', 'groups', 'region', 'phone', 'password', 'first_password')
        model = User
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'validators': [EmailValidator, ]},
            'phone': {'validators': []}
        }
        read_only_fields = ('groups', 'first_password')

    def create(self, validated_data):
        images = self.context.get('view').request.FILES
        return create_user(user_data=validated_data, pk=validated_data['groups'], images=images)


class LockUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('pk', 'email', 'groups', 'region')
        model = User
        read_only_fields = ('pk', 'email', 'groups', 'region')

    def update(self, instance, validated_data):
        instance.groups = 5
        instance.save()
        return instance


class LockRPSerializer(serializers.ModelSerializer):

    user = LockUserSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = RPProfile
        read_only_fields = ('first_name', 'last_name', 'second_name', 'phone', 'status', 'first_rp', 'user')

    def update(self, instance, validated_data):
        change_lock_rp(instance.user, validated_data['zam'], instance.first_rp)
        instance.user.delete()
        return instance


class LockExecutorSerializer(serializers.ModelSerializer):
    user = LockUserSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = ExecutorProfile
        read_only_fields = ('first_name', 'last_name', 'second_name', 'phone', 'status', 'rp')

    def update(self, instance, validated_data):
        instance.user.groups = Group.objects.get(pk=5)
        instance.user.save()
        instance.status = 2
        instance.save()
        reset_executor(instance.user)

        return instance


class AdminSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = AdminProfile
        fields = '__all__'

    def create(self, validated_data):
        return AdminProfile.objects.create(
            user=create_user(user_data=validated_data.pop('user'), pk=1),
            **validated_data
        )

    def update(self, instance, validated_data):
        return update_user(instance=instance, validated_data=validated_data)


class RPSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = RPProfile
        fields = '__all__'
        read_only_fields = ('status', 'zam',)

    def create(self, validated_data):
        return RPProfile.objects.create(
            user=create_user(user_data=validated_data.pop('user'), pk=2),
            **validated_data
        )

    def update(self, instance, validated_data):
        validated_data.pop('first_rp')
        return update_user(instance=instance, validated_data=validated_data)


class ExecutorSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)
    rating = RatingSerializer(read_only=True)

    class Meta:
        model = ExecutorProfile
        fields = '__all__'
        read_only_fields = ('rp', 'status',)

    def create(self, validated_data):
        return ExecutorProfile.objects.create(
            user=create_user(user_data=validated_data.pop('user'), pk=3),
            **validated_data
        )

    def update(self, instance, validated_data):
        return update_user(instance=instance, validated_data=validated_data)


class CustomerSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = CustomerProfile
        fields = '__all__'

    def create(self, validated_data):
        return CustomerProfile.objects.create(
            user=create_user(user_data=validated_data.pop('user'), pk=4),
            **validated_data
        )

    def update(self, instance, validated_data):
        return update_user(instance=instance, validated_data=validated_data)


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('pk', 'password', 'first_password')
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ('first_password',)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.first_password = False
        instance.save()

        return instance
