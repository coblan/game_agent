# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2021-01-03 00:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0019_storerecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameblock',
            name='charge_api',
            field=models.CharField(blank=True, max_length=200, verbose_name='充值接口'),
        ),
        migrations.AddField(
            model_name='gameblock',
            name='db',
            field=models.CharField(blank=True, max_length=50, verbose_name='数据库'),
        ),
        migrations.AlterField(
            model_name='gameplayer',
            name='history_credit',
            field=models.IntegerField(default=0, verbose_name='累计积分'),
        ),
    ]
