# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zines', '0006_issue_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='zine',
            name='zine_pic',
            field=models.URLField(blank=True),
        ),
    ]
