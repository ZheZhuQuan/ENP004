# Generated by Django 3.0.8 on 2020-08-12 06:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('profile_app', '0002_auto_20200811_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth',
            field=models.DateField(default=datetime.datetime(1992, 8, 12, 15, 14, 52, 54579), verbose_name='生年月日'),
        ),
    ]
