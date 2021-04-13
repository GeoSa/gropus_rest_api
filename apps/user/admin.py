from django.contrib import admin
from .models import User, AdminProfile, RPProfile, ExecutorProfile, CustomerProfile

admin.site.register(User)
admin.site.register(AdminProfile)
