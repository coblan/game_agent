from django.db import models
from django.contrib.auth.models import Group,User

# Create your models here.

class AgentUser(models.Model):
    name = models.CharField('代理人名字',max_length=100,)
    account = models.OneToOneField(User,verbose_name='账号',null=True)
    amount = models.IntegerField(verbose_name='余额',default=0)
    regist_code = models.CharField('注册码',max_length=20,blank=True,)
    qq = models.CharField('QQ号码',max_length=20,blank=True)
    
    def __str__(self):
        return self.name

class GamePlayer(models.Model):
    acount = models.CharField('玩家账号',max_length=100,)
    agent= models.ForeignKey(AgentUser,verbose_name='代理人')
    new_guy_gift = models.BooleanField(verbose_name='新人福利',default=False)
    credit = models.IntegerField(verbose_name='积分',default=0)
    history_credit = models.IntegerField(verbose_name='累计积分',default=0)
    has_get = models.CharField('已领取',max_length=200,blank=True)
    desp = models.CharField('备注',max_length=300,blank=True)
    createtime = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    def __str__(self):
        return self.acount

class Game(models.Model):
    name = models.CharField('游戏名称',max_length = 100)
    
    def __str__(self):
        return self.name

class GameBlock(models.Model):
    name = models.CharField('大区名字',max_length=200)
    game = models.ForeignKey(to=Game,verbose_name='游戏',null=True)
    
    def __str__(self):
        return self.name

RECHARGE_STATUS = (
    (0,'未成功'),
    (1,'成功'),
)

class Recharge(models.Model):
    agent= models.ForeignKey(AgentUser,verbose_name='代理人')
    #game = models.IntegerField(verbose_name='游戏',default=0)
    game = models.ForeignKey(to=Game,verbose_name='游戏',null=True)
    #block = models.IntegerField(verbose_name='大区',default= 0 )
    block = models.ForeignKey(to=GameBlock, verbose_name='大区')
    player = models.ForeignKey(GamePlayer,verbose_name='玩家',)
    charactar = models.CharField('角色',max_length=100,blank=True)
    pc_id = models.BigIntegerField(verbose_name='角色id',default=0)
    #player = models.CharField('用户名',max_length=100,)
    desp = models.TextField('产品描述',blank= True)
    amount = models.IntegerField('数量',default=0)
    createtime= models.DateTimeField(verbose_name='充值时间',auto_now_add=True)
    status = models.IntegerField(verbose_name='状态',default=1)


class AgentRecharge(models.Model):
    agent = models.ForeignKey(AgentUser,verbose_name='代理人')
    amount = models.IntegerField(verbose_name='充值金额')
    createtime= models.DateTimeField(verbose_name='充值时间',auto_now_add=True)
    admin = models.ForeignKey(User,verbose_name='操作人员',null=True)


class StoreRecord(models.Model):
    player = models.ForeignKey(to=GamePlayer,verbose_name='购买人')
    character = models.CharField('角色',max_length=100,)
    code = models.CharField(verbose_name='物品代码',max_length=50)
    credit = models.IntegerField('耗费积分',default=0)
    createtime= models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    
    
