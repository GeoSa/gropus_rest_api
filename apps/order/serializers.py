from datetime import datetime
from rest_framework import serializers
from .models import Order, Review, ReviewImages, ReviewScans
from ..user.models import ExecutorProfile
from ..rating.models import Rating
from .payments import payments
from .utils import get_order_amount, update_order, create_notification


class ReviewImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewImages
        fields = '__all__'


class ReviewScansSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewScans
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    images = ReviewImagesSerializer(many=True, required=False)
    scans = ReviewScansSerializer(many=True, required=False)

    class Meta:
        model = Review
        fields = ('pk', 'images', 'scans', 'description', 'order', 'user')
        read_only_fields = ('images', 'scans', 'user',)

    def create(self, validated_data, pk=None):
        images_data = self.context.get('view').request.FILES
        images = images_data.pop('images')
        scans = images_data.pop('scans')

        review = Review.objects.create(
            description=validated_data['description'],
            user=validated_data['order'].executor,
            order=validated_data['order'],
        )

        for image in images:
            ReviewImages.objects.create(review=review, images=image)

        for scan in scans:
            ReviewScans.objects.create(review=review, scans=scan)

        update_order(validated_data=validated_data)

        if str(validated_data['user'].groups) == 'executor':
            create_notification(3, validated_data['description'], validated_data['order'])

        return review

    def update(self, instance, validated_data):

        images_data = self.context.get('view').request.FILES
        images = images_data.pop('images')
        scans = images_data.pop('scans')

        for image in images:
            ReviewImages.objects.create(review=instance, images=image)

        for scan in scans:
            ReviewScans.objects.create(review=instance, scans=scan)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        update_order(validated_data=validated_data)
        return instance


class FullOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'pk',
            'customer_number',
            'customer_address',
            'customer',
            'region',
            'city',
            'status',
            'created_by',
            'order_type',
            'order_source',
            'order_amount',
            'valid',
        )
        extra_fields = {'created_by': {'required': False}}
        read_only_fields = ('pk', 'order_amount', 'valid', 'status', 'created_by',)

    def create(self, validated_data):
        if 'order_source' not in validated_data:
            validated_data['order_source'] = 2
        return Order.objects.create(
            **validated_data,
            created_by=self.request.user,
            order_amount=get_order_amount(validated_data=validated_data))

    def update(self, instance, validated_data):
        instance.customer_number = validated_data['customer_number']
        instance.customer_address = validated_data['customer_address']
        instance.valid = True
        instance.start_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        instance.order_amount = get_order_amount(validated_data=validated_data)
        instance.save()

        return instance


class AcceptValidOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('valid',)
        read_only_fields = ('valid',)

    def update(self, instance, validated_data=None):
        instance.valid = True
        instance.status = 2
        instance.save()
        return instance


class DeclineValidOrderSerializer(serializers.ModelSerializer):

    description_field = serializers.CharField(source='description')

    class Meta:
        model = Order
        fields = ('valid', 'description_field')
        read_only_fields = ('valid',)

    def update(self, instance, validated_data=None):
        instance.valid = False
        instance.start_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        instance.save()
        create_notification(tp=1, description=validated_data['description'], order=instance)

        return instance


class ExecutorTakeOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            'pk',
            'customer_number',
            'customer_address',
            'customer',
            'region',
            'city',
            'status',
            'created_by',
            'order_type',
            'order_source',
            'order_amount',
            'valid',
            'executor',
        )
        read_only_fields = (
            'pk',
            'customer_number',
            'customer_address',
            'customer',
            'region',
            'city',
            'status',
            'created_by',
            'order_type',
            'order_source',
            'order_amount',
            'valid',
            'executor',
        )

    def update(self, instance, validated_data):
        print(validated_data['executor'].groups)

        if str(validated_data['executor'].groups) == 'executor':
            executor = ExecutorProfile.objects.get(user=validated_data['executor'].id)
            try:
                rating = Rating.objects.get(user=executor)
                rating.orders += 1
                rating.save()
            except Rating.DoesNotExist:
                Rating.objects.create(user=executor, orders=1)
            instance.rp = executor.rp
        elif str(validated_data['executor'].groups) == 'regional representative':
            instance.rp = validated_data['executor']

        instance.executor = validated_data['executor']
        instance.start_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        instance.status = 2
        instance.save()
        return instance


class DeclineReviewSerializer(serializers.ModelSerializer):

    description = serializers.CharField(max_length=255, allow_null=True)

    class Meta:
        model = Order
        fields = ('approve_time', 'description')
        read_only_fields = ('approve_time',)

    def update(self, instance, validated_data=None):

        instance.approve_status = 2
        instance.moderation_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        instance.save()

        create_notification(tp=2, description=validated_data['description'], order=instance)

        return instance


class AcceptReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('approve_time',)
        read_only_fields = ('approve_time',)

    def update(self, instance, validated_data=None):
        instance.approve_status = 1
        instance.status = 4
        if instance.moderation_time:
            instance.repeat_moderation_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        else:
            instance.moderation_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        instance.save()

        if str(instance.executor.groups) == 'executor':
            rating = Rating.objects.get(user=ExecutorProfile.objects.get(pk=instance.executor))
            rating.closed_orders += 1
            rating.save()

        payments(instance.id)

        return instance

