import os
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()
from django.contrib.auth.models import Group

GROUPS = ['admin', 'regional representative', 'executor', 'customer', 'locked']
MODELS = ['user']

for group in GROUPS:
    new_group, created = Group.objects.get_or_create(name=group)
