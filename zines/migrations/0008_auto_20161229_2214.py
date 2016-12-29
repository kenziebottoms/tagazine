# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zines', '0007_zine_zine_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='date_published',
            new_name='pub_date',
        ),
        migrations.AddField(
            model_name='issue',
            name='cover',
            field=models.URLField(blank=True),
        ),
    ]
