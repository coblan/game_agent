
from helpers.mobile.shortcut import FieldsMobile,ModelTableMobile
from helpers.director.shortcut import director
from hello.engin_menu import mb_page
from django.utils.translation import ugettext as _
from agent.models import Game,GameBlock,GamePlayer,EverdaySign
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
            {'name':'history',
             'label':_('查看历史'),
             'editor':'com-btn',
             'show_express':'rt = scope.vc.row.player',
             'type':'info',
             'click_express':'scope.head.table_ctx.search_args.player=scope.ps.vc.row.player;live_root.open_live("live_list",scope.head.table_ctx)',
             'table_ctx':{
                 'title':_('签到历史'),
                 'search_args':{},
                 **EveryDayHistory().get_head_context()},
             },
            {'name':'invite-btn',
             'label':_('复制邀请链接'),
             'editor':'com-btn',
             'show_express':'rt = scope.vc.row.player',
             'click_express':''' ex.copyToClip(scope.ps.vc.row.invite).then(()=>{cfg.toast("复制成功")})'''} # setTimeout(()=>{document.execCommand('copy');cfg.toast("复制成功!")},500);
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
            EverdaySign.objects.create(player = player)
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
        pass

class EveryDayHistory(ModelTableMobile):
    model = EverdaySign
    exclude =['id']
    nolimit=True
    def inn_filter(self, query):
        return query.filter(player_id=self.kw.get('player'))
    


director.update({
    'everyday-sign':EveryDaySignForm,
    'everyday-sign-history':EveryDayHistory
})    


mb_page.update({
    'everyday':EveryDaySign
})