from .models import User, RPProfile, ExecutorProfile, Group
from apps.order.models import Order
from apps.wallet.models import Wallet


def create_user(user_data, pk, images):
    if images:
        face_photo = images.pop('face_photo')
        passport_photo = images.pop('passport_photo')
        adr_photo = images.pop('adr_photo')

        user = User.objects.create(
            **user_data,
            groups=Group.objects.get(pk=pk),
            face_photo=face_photo,
            passport_photo=passport_photo,
            adr_photo=adr_photo
        )
    else: user = User.objects.create(**user_data, groups=Group.objects.get(pk=pk))

    if pk == 3 or pk == 2:
        user.first_password = True
    user.is_staff = True
    user.set_password(user_data['password'])
    user.save()
    Wallet.objects.create(user=user)

    return user


def update_user(instance, validated_data):
    user_data = validated_data.pop('user')
    for attr, value in user_data.items():
        setattr(instance.user, attr, value)
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()
    instance.user.save()

    return instance


def change_lock_rp(rp, zam, first_rp: bool):

    orders = Order.objects.filter(rp=rp, archive=False)

    for order in orders:
        if order.rp == order.executor:
            order.executor = zam
        order.rp = zam
        order.save()

    del orders

    executors = ExecutorProfile.objects.filter(rp=rp)

    for executor in executors:
        executor.rp = zam
        executor.save()

    del executors

    zam_profile = ExecutorProfile.objects.get(user=zam)
    zam.groups = rp.groups
    zam.save()

    RPProfile.objects.create(
        user=zam,
        first_name=zam_profile.first_name,
        last_name=zam_profile.last_name,
        second_name=zam_profile.second_name,
        first_rp=first_rp,
    )

    zam_profile.delete()


def reset_executor(executor):

    orders = Order.objects.filter(executor=executor, archive=False)

    for order in orders:
        order.executor = None
        order.rp = None
        order.start_time = None
        order.valid = True
        order.status = 1
        order.save()
