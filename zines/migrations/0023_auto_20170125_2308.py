# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-25 23:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zines', '0022_page'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='page',
            order_with_respect_to='issue',
        ),
    ]
