# Generated by Django 3.1 on 2021-12-16 20:10

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardens', '0003_auto_20211202_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='garden',
            name='geom_point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='garden',
            name='geom_polygon',
            field=django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='garden',
            name='description',
            field=models.TextField(max_length=1000),
        ),
    ]