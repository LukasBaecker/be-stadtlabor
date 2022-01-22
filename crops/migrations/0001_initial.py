# Generated by Django 3.1 on 2021-11-28 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('crop_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('characteristics', models.TextField(max_length=500)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]