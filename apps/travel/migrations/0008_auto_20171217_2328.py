# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-17 23:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0007_auto_20171217_2317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='created_user',
            new_name='created_by',
        ),
    ]
