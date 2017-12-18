# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-17 23:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0006_auto_20171217_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='attendees',
            field=models.ManyToManyField(related_name='trips', to='travel.User'),
        ),
    ]
