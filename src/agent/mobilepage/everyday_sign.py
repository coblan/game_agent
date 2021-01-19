
from helpers.mobile.shortcut import FieldsMobile,ModelTableMobile
from helpers.director.shortcut import director
from hello.engin_menu import mb_page
from django.utils.translation import ugettext as _
from agent.models import Game,GameBlock,GamePlayer,EverdaySign
from django.utils import timezone

class EveryDaySign(object):
    def get_template(self):
        return 'mobile/live_show.html'
    
    def __init__(self, request, engin):
        pass
    
    def get_context(self):
        return {
            'editor':'live_page',
            'editor_ctx':{
                'head':{
                    'editor':'com-lay-navbar',
                    'title':'今日签到',
                },
                'bodys':[
                    {'editor':'com-fields-panel',
                     **EveryDaySignForm().get_context(),
                     #'after_save_express':'debugger;alert("bb")'
                     'after_save_express':'if(scope.row.msg){cfg.toast(scope.row.msg)}else{cfg.toast("打卡成功")}'
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
        ops.append(
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
             }
        )
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
             }
        ]
    
    def dict_row(self):
        if getattr(self,'player',None):
            return {
                'player':self.player.id,
                'msg':self.msg,
                #'already_signed':self.already_signed
            }
        else:
            return {}
            
    
    def save_form(self):
        try:
            player = GamePlayer.objects.get(block_id = self.kw.get('block'),acount=self.kw.get('account'))
            self.player= player
            now = timezone.now()
            if not EverdaySign.objects.filter(createtime__date = timezone.now().date(),player=player).exists():
                EverdaySign.objects.create(player = player)
                self.msg = ''
            else:
                self.msg = _('您今天已经签到过了!')
                #raise UserWarning(_('您今天已经打过卡了!') )
        except GamePlayer.DoesNotExist:
            raise UserWarning(_('该游戏分区下不存在该玩家!'))
        

class EveryDayHistory(ModelTableMobile):
    model = EverdaySign
    exclude =['id']
    
    def inn_filter(self, query):
        return query.filter(player_id=self.kw.get('player'))
    


director.update({
    'everyday-sign':EveryDaySignForm,
    'everyday-sign-history':EveryDayHistory
})    


mb_page.update({
    'everyday':EveryDaySign
})