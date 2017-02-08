# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-08 23:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zines', '0027_auto_20170208_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(editable=False, unique=True),
        ),
    ]