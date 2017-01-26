# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 23:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zines', '0017_auto_20170116_0614'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('member_since', models.DateField(verbose_name=b'Member since')),
                ('name', models.CharField(blank=True, max_length=500)),
                ('bio', models.TextField(blank=True)),
                ('website', models.URLField(blank=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('pic', models.FileField(blank=True, upload_to=b'users')),
            ],
        ),
        migrations.RemoveField(
            model_name='authorship',
            name='user',
        ),
        migrations.AlterField(
            model_name='issue',
            name='guest_authors',
            field=models.ManyToManyField(blank=True, to='zines.Profile'),
        ),
        migrations.AlterField(
            model_name='zine',
            name='authors',
            field=models.ManyToManyField(through='zines.Authorship', to='zines.Profile'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='authorship',
            name='user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='zines.Profile'),
            preserve_default=False,
        ),
    ]