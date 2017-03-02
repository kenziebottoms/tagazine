# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-16 23:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zines', '0029_auto_20170216_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='zine',
            name='primary_language',
            field=models.CharField(default=b'English', max_length=300),
        ),
        migrations.AlterField(
            model_name='zine',
            name='external',
            field=models.BooleanField(default=False, verbose_name=b'Externally hosted'),
        ),
    ]