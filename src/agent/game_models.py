# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class TbCharacter(models.Model):
    pc_id = models.BigIntegerField(primary_key=True)
    account_id = models.CharField(max_length=32)
    grade = models.SmallIntegerField()
    pc_name = models.CharField(max_length=24)
    race = models.SmallIntegerField()
    gender = models.SmallIntegerField()
    class_field = models.SmallIntegerField(db_column='class')  # Field renamed because it was a Python reserved word.
    hair_id = models.CharField(max_length=8)
    face_id = models.CharField(max_length=8)
    tail_id = models.CharField(max_length=8)
    pc_level = models.IntegerField()
    pc_exp = models.BigIntegerField()
    hongmoon_level = models.IntegerField()
    hongmoon_exp = models.BigIntegerField()
    pc_hp = models.IntegerField()
    pc_mana = models.IntegerField()
    pc_ability_hp = models.IntegerField(blank=True, null=True)
    pc_hosin_hp = models.IntegerField()
    pc_ability_power = models.FloatField()
    pc_ability_power_max = models.FloatField()
    hongmoon_attack = models.IntegerField()
    hongmoon_defence = models.IntegerField()
    login_time = models.BigIntegerField()
    logout_time = models.BigIntegerField()
    create_time = models.BigIntegerField()
    update_time = models.BigIntegerField()
    changename_time = models.BigIntegerField()
    changebody_time = models.BigIntegerField()
    delete_flag = models.BooleanField()
    delete_time = models.BigIntegerField()
    migration_flag = models.BooleanField()
    migration_step = models.SmallIntegerField()
    locker_flag = models.BooleanField()
    locker_takeout_time = models.BigIntegerField()
    grade_time = models.BigIntegerField()
    total_play_time = models.BigIntegerField()
    today_play_time = models.BigIntegerField()
    user_type = models.SmallIntegerField()
    user_type_expire_time = models.BigIntegerField()
    dw_update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tb_character'