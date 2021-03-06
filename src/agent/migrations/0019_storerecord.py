# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-21 19:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0018_gameplayer_history_credit'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.CharField(max_length=100, verbose_name='角色')),
                ('code', models.CharField(max_length=50, verbose_name='物品代码')),
                ('credit', models.IntegerField(default=0, verbose_name='耗费积分')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.GamePlayer', verbose_name='购买人')),
            ],
        ),
    ]
