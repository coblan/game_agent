# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-07 01:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0002_auto_20201107_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentuser',
            name='account',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='账号'),
        ),
    ]
