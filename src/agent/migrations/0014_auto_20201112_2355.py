# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-12 23:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0013_gameplayer_new_guy_gift'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplayer',
            name='credit',
            field=models.IntegerField(default=0, verbose_name='积分'),
        ),
        migrations.AlterField(
            model_name='gameplayer',
            name='new_guy_gift',
            field=models.BooleanField(default=False, verbose_name='新人福利'),
        ),
    ]
