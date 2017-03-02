# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-02 21:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zines', '0032_auto_20170217_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='thumb',
            field=models.ImageField(blank=True, upload_to=b'issues'),
        ),
        migrations.AddField(
            model_name='page',
            name='thumb',
            field=models.ImageField(blank=True, upload_to=b'issues'),
        ),
        migrations.AddField(
            model_name='zine',
            name='thumb',
            field=models.ImageField(blank=True, upload_to=b'covers'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='cover',
            field=models.ImageField(blank=True, upload_to=b'issues'),
        ),
        migrations.AlterField(
            model_name='page',
            name='content',
            field=models.ImageField(upload_to=b'issues'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='member_since',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='zine',
            name='cover',
            field=models.ImageField(upload_to=b'covers'),
        ),
    ]