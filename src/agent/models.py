from django.db import models
from django.contrib.auth.models import Group,User
# Create your models here.

class AgentUser(models.Model):
    name = models.CharField('代理人名字',max_length=100,)
    account = models.OneToOneField(User,verbose_name='账号',null=True)
    
    def __str__(self):
        return self.name

class Recharge(models.Model):
    agent= models.ForeignKey(AgentUser,verbose_name='代理人')
    game = models.IntegerField(verbose_name='游戏',default=0)
    block = models.IntegerField(verbose_name='大区',default= 0 )
    player = models.CharField('用户名',max_length=100,)
    desp = models.TextField('产品描述',blank= True)
    amount = models.IntegerField('数量',default=0)
    createtime= models.DateTimeField(verbose_name='充值时间',auto_now_add=True)
    status = models.IntegerField(verbose_name='状态',default=0)

