# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-07 14:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0003_auto_20201107_0125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.IntegerField(default=0, verbose_name='游戏')),
                ('block', models.IntegerField(default=0, verbose_name='大区')),
                ('player', models.CharField(max_length=100, verbose_name='用户名')),
                ('desp', models.TextField(blank=True, verbose_name='产品描述')),
                ('amount', models.IntegerField(default=0, verbose_name='数量')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='充值时间')),
                ('status', models.IntegerField(default=0, verbose_name='状态')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.AgentUser', verbose_name='代理人')),
            ],
        ),
    ]
