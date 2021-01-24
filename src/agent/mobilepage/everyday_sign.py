
from helpers.mobile.shortcut import FieldsMobile,ModelTableMobile
from helpers.director.shortcut import director
from hello.engin_menu import mb_page
from django.utils.translation import ugettext as _
from agent.models import Game,GameBlock,GamePlayer,EverdaySign,RechargeBonus
from django.utils import timezone
import base64
from agent.game_utile import check_account_exist

class EveryDaySign(object):
    need_login=False
    def get_template(self):
        return 'mobile/live_show.html'
    
    def __init__(self, request, engin):
        self.request = request
    
    def get_context(self):
        kws= EveryDaySignForm().get_context()
        if self.request.GET.get('par') and self.request.GET.get('block'):
            par_account = base64.b64decode( self.request.GET.get('par') ).decode('utf-8')
            block = self.request.GET.get('block')
            par_player = GamePlayer.objects.get(acount=par_account,block_id=block)
            kws['row']['par'] = par_player.id
        return {
            'editor':'live_page',
            'editor_ctx':{
                'head':{
                    'editor':'com-lay-navbar',
                    'title':'今日签到',
                },
                'bodys':[
                    {'editor':'com-fields-panel',
                     **kws,
                     #**EveryDaySignForm().get_context(),
                     #'after_save_express':'debugger;alert("bb")'
                     'after_save_express':'scope.vc.row.invite = location.origin+scope.row.invite_path;if(scope.row.msg){cfg.toast(scope.row.msg)}else{cfg.toast("打卡成功")};'
                     }
                ]
            }
        }
    
class EveryDaySignForm(FieldsMobile):
    nolimit = True
    
    def get_operations(self):
        ops = super().get_operations()
        for op in ops:
            op['label'] = _('签到')
            op['type'] ='danger'
        ops.extend([
            #{'name':'history',
             #'label':_('查看历史'),
             #'editor':'com-btn',
             #'show_express':'rt = scope.vc.row.player',
             #'type':'info',
             #'click_express':'scope.head.table_ctx.search_args.player=scope.ps.vc.row.player;live_root.open_live("live_list",scope.head.table_ctx)',
             #'table_ctx':{
                 #'title':_('签到历史'),
                 #'search_args':{},
                 #**EveryDayHistory().get_head_context()},
             #},
            {'name':'invite-btn',
             'label':_('复制邀请链接'),
             'editor':'com-btn',
             'show_express':'rt = scope.vc.row.player',
             'click_express':''' ex.copyToClip(scope.ps.vc.row.invite).then(()=>{cfg.toast("复制成功")})'''
             }   ,
            {'name':'history',
            'label':_('积分奖励'),
            'editor':'com-btn',
            'type':'info',
            'show_express':'rt = scope.vc.row.player',
            'click_express':''' ex.each(scope.head.tab_ctx.items,item=>{if(item.search_args){item.search_args.player=scope.ps.vc.row.player}});
            live_root.open_live("live_tab",scope.head.tab_ctx)''',
            'tab_ctx':{
                'title':_('积分奖励'),
                'items':[
                    {'name':'1',
                     'label':_('签到奖励'),
                     'editor':'com-top-list',
                     'search_args':{},
                      **EveryDayHistory().get_head_context()  
                     },
                    {'name':'2',
                     'label':_('推介奖励'),
                      'editor':'com-top-list',
                     'search_args':{},
                      **RechargeBonusTab().get_head_context()  
                     },
                    #{'name':'3','label':'测试三'},
                    #{'name':'4','label':'测试四'},
                    #{'name':'5','label':'测试五'},
                    #{'name':'6','label':'测试六'},
                    #{'name':'7','label':'测试七'},
                    #{'name':'8','label':'测试八'},
                    #{'name':'9','label':'测试九'},
                    #{'name':'10','label':'测试十'},
                    #{'name':'11','label':'测试十一'},
                    #{'name':'12','label':'测试十二'},
                    #{'name':'13','label':'测试十三'},
                    #{'name':'14','label':'测试十四'},
                ] 
             },
            }  
        ])
        return ops
    
    def get_heads(self):
        return [
           {'name':'game','editor':'com-field-select','label':_('游戏'),'required':True,'options':[
                {'value':x.pk,'label':str(x)} for x in Game.objects.all()
                ]},
            {'name':'block','editor':'com-field-select',
             'options':[{'value':x.pk,'label':str(x)} for x in GameBlock.objects.all()],
             'label':_('区服'),'required':True},
            {'name':'account','editor':'com-field-linetext',
             'label':_('账号'),'required':True,
             },
            {'name':'invite','editor':'com-field-blocktext','readonly':True,
             'label':_('邀请玩家'),
             'show_express':'rt = scope.row.player'}
        ]
    
    def dict_row(self):
        if getattr(self,'player',None):
            return {
                'player':self.player.id,
                'msg':self.msg,
                'invite':'',
                'invite_path':'/mb/everyday?par=%s&block=%s'%( base64.b64encode(self.player.acount.encode('utf-8') ).decode('utf-8') , self.player.block_id)
                #'already_signed':self.already_signed
            }
        else:
            return {}
            
    
    def save_form(self):
        try:
            player = GamePlayer.objects.get(block_id = self.kw.get('block'),acount=self.kw.get('account'))
        except GamePlayer.DoesNotExist:
            if self.kw.get('par'):
                if check_account_exist(account=self.kw.get('account'), block=self.kw.get('block')):
                    par_player= GamePlayer.objects.get(pk=self.kw.get('par'))
                    player = GamePlayer.objects.create(par= par_player,
                                                       acount=self.kw.get('account'),
                                                       block_id = self.kw.get('block'),
                                                       agent=par_player.agent)
                else:
                    raise UserWarning(_('该游戏分区下不存在该玩家!'))
            else:
                raise UserWarning(_('新用户请使用玩家邀请链接,或者首先联系代理人为你充值!'))
        
        self.player= player
        now = timezone.now()
        if not EverdaySign.objects.filter(createtime__date = timezone.now().date(),player=player).exists():
            #EverdaySign.objects.create(player = player)
            self.pay_score()
            self.msg = ''
        else:
            self.msg = _('您今天已经签到过了!')
            #raise UserWarning(_('您今天已经打过卡了!') )

    def pay_score(self):
        '''
        玩家签到规则：
签到1次：20积分；

连续签到7天：额外奖励50积分

连续签到15天：额外奖励200积分

连续签到30天：额外奖励500积分

连续签到的可以叠加。每30天重置1次

连续签到不能中断，中断了就从第一天开始算。每签到1次20积分固定！
        '''

        ago_30 = timezone.now() - timezone.timedelta(days=30)
        if self.player.last_settle_date and self.player.last_settle_date >= ago_30.date():
            query = EverdaySign.objects.filter(createtime__date__gt= self.player.last_settle_date).order_by('-createtime')
        else:
            query = EverdaySign.objects.filter(createtime__date__gte=ago_30.date()).order_by('-createtime')
        last_inst = None
        count = 1
        for inst in query:
            if not last_inst:
                last_inst = inst
                if last_inst.createtime.date() == timezone.now().date() -timezone.timedelta(days=1):
                    count += 1
                else:
                    break
            else:
                if last_inst .createtime.date()== inst.createtime.date() + timezone.timedelta(days=1):
                    count  += 1
                    last_inst = inst
                else:
                    break
                
        credit_bonus =20    
        memo='签到20;'
        if count ==7:
            credit_bonus += 50
            memo+='连续7日+50;'
        elif count ==15:
            credit_bonus += 200
            memo+='连续15日+200;'
        elif count ==30:
            credit_bonus += 500
            memo+='连续30日+500;'
            self.player.last_settle_date = timezone.now().date()
        else:
            memo +='连续%s日'%count
        EverdaySign.objects.create(player = self.player,memo=memo,amount =credit_bonus)
        self.player.credit += credit_bonus
        self.player.save()
            
                
        

class EveryDayHistory(ModelTableMobile):
    model = EverdaySign
    exclude =['id']
    nolimit=True
    fields_sort=['memo','createtime']
    
    def dict_head(self, head):
        width ={
            'memo':'3rem',
        }
        if head['name'] in width:
            head['width'] =width[head['name']]
        return head
    
    def inn_filter(self, query):
        return query.filter(player_id=self.kw.get('player'))
    

class RechargeBonusTab(ModelTableMobile):
    model = RechargeBonus
    nolimit = True
    fields_sort=['amount','createtime']
    
    def dict_head(self, head):
        width ={
            'amount':'3rem',
        }
        if head['name'] in width:
            head['width'] =width[head['name']]
        return head
    
    def inn_filter(self, query):
        return query.filter(player_id=self.kw.get('player'))


director.update({
    'everyday-sign':EveryDaySignForm,
    'everyday-sign-history':EveryDayHistory,
    'recharge-bonus':RechargeBonusTab,
})    


mb_page.update({
    'everyday':EveryDaySign
})