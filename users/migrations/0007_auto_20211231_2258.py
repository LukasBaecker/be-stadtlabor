# Generated by Django 3.1 on 2021-12-31 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20211218_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordreset',
            name='email',
            field=models.CharField(max_length=255),
        ),
    ]
