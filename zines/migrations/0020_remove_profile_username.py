# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-18 00:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zines', '0019_remove_profile_member_since'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='username',
        ),
    ]