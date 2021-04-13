# Generated by Django 3.0.1 on 2020-10-03 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_first_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminprofile',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='customerprofile',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='executorprofile',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='rpprofile',
            name='phone',
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]