# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-08 00:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0007_auto_20201107_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='游戏名称')),
            ],
        ),
        migrations.CreateModel(
            name='GameBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='大区名字')),
            ],
        ),
        migrations.AlterField(
            model_name='recharge',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.GameBlock', verbose_name='大区'),
        ),
        migrations.AlterField(
            model_name='recharge',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='agent.Game', verbose_name='游戏'),
        ),
    ]
