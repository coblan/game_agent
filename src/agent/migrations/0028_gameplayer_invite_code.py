# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2021-01-24 22:24
from __future__ import unicode_literals

from django.db import migrations
import helpers.director.model_func.cus_fields.char_id


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0027_auto_20210124_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplayer',
            name='invite_code',
            field=helpers.director.model_func.cus_fields.char_id.CharIdField(blank=True, max_length=50, verbose_name='邀请码'),
        ),
    ]
