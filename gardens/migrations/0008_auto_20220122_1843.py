# Generated by Django 3.1 on 2022-01-22 17:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gardens', '0007_auto_20211231_2258'),
    ]

    operations = [
        migrations.RemoveField(
    model_name='garden',
    name='members',
),
migrations.AddField(
    model_name='garden',
    name='members',
    field=models.ManyToManyField(blank = True, related_name='gardens', to=settings.AUTH_USER_MODEL),
),
    ]

