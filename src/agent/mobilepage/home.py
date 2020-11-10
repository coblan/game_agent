from hello.engin_menu import mb_page
from helpers.director.shortcut import Fields,director,director_view,get_request_cache
from helpers.mobile.shortcut import FieldsMobile
from agent.game_models import TbCharacter
from agent.models import GameBlock,GamePlayer,Recharge,Game
from django.core.exceptions import PermissionDenied 

class Home(object):
    def __init__(self, request, engin):
        if not getattr(request.user,'agentuser',None):
            raise PermissionDenied('您不是代理人用户')
    
    def get_template(self):
        return 'mobile/live_show.html'
    
    def get_context(self):
        return {
            'editor':'live_cell',
            'editor_ctx':  { 'title':'代理人系统',
                             'cells':[
                                 {'label':'玩家充值',
                                  'fields_ctx':{**RechargeForm().get_head_context(),
                                                'title':'玩家充值'},
                                  'click_express':'live_root.open_live(live_fields,scope.head.fields_ctx)'},
                                 {'label':'新人福利',
                                   'fields_ctx':{**NewPlayerGift().get_head_context(),
                                                'title':'新人福利'},
                                  'click_express':'live_root.open_live(live_fields,scope.head.fields_ctx)'},
                             ],
                             'bottom_editors':[
                                 {'label':'退出登录','click_express':'location="/accounts/logout?next=/mb/home"','editor':'com-btn','type':'warning',
                                  'css':'.logout-btn{width: 74vw;margin: 13vw;margin-top: 1rem}','class':"logout-btn"}
                             ]
                           }
        }    
    

class RechargeForm(FieldsMobile):
    
    #def get_operations(self):
        #ops = super().get_operations()
        #ops += [
            #{'name':'quit','label':'退出登录','click_express':'location="/accounts/logout?next=/mb/home"','editor':'com-btn','type':'default'}
        #]
        #return ops
    
    def get_heads(self):
        return [
            {'name':'game','editor':'com-field-select','label':'游戏','required':True,'options':[
                {'value':x.pk,'label':str(x)} for x in Game.objects.all()
                ]},
            {'name':'block','editor':'com-field-select',
             'options':[{'value':x.pk,'label':str(x)} for x in GameBlock.objects.all()],
             'label':'区服','required':True},
            {'name':'account','editor':'com-field-linetext',
             #'mounted_express':'scope.vc.$on("blur",(e)=>{live_root.$emit("account_change",e)})',
             'label':'账号','required':True},
            {'name':'character','editor':'com-field-select','options':[],
             'mounted_express':'''scope.vc.$watch("row.account",v=>{if(v){cfg.show_load();ex.director_call("get_charecter",{account:v}).then(options=>{cfg.hide_load();if(options.length==0){cfg.toast("没有找到对应角色")}else{  scope.vc.head.options=options   }})       }     } )
             scope.vc.$watch("row.character",v=>{  if(v){ var opt = ex.findone(scope.vc.head.options,{value:v}); scope.vc.row._character_label = opt.label  }   })
             ''' ,
             'label':'角色','required':True},
            {'name':'amount','editor':'com-field-int','label':'当前余额','readonly':True},
            {'name':'recharge_amount','editor':'com-field-int','label':'充值金额','required':True,'fv_rule':'integer(+)'},
        ]
    
    def dict_row(self):
        return {
            'amount':self.crt_user.agentuser.amount
        }
    
    def clean(self):
        if self.kw.get('recharge_amount') > self.kw.get('amount'):
            self.add_error('recharge_amount','充值金额不够')

    
    def save_form(self):
        self.crt_user.agentuser.amount  -= self.kw.get('recharge_amount')
        if self.crt_user.agentuser.amount <0:
            raise UserWarning('余额不足')
        self.crt_user.agentuser.save()
        player = GamePlayer.objects.get(acount=self.kw.get('account'))
        Recharge.objects.create(agent=self.crt_user.agentuser,game_id=self.kw.get('game'),
                                block_id=self.kw.get('block'),
                                player=player,
                                charactar=self.kw.get('_character_label'),
                                pc_id=self.kw.get('character'),
                                amount=self.kw.get('recharge_amount'),
                                status=1)
       

class NewPlayerGift(FieldsMobile):
    def get_heads(self):
        return [
             {'name':'game','editor':'com-field-select','label':'游戏','required':True,'options':[
                {'value':x.pk,'label':str(x)} for x in Game.objects.all()
                ]},
            {'name':'block','editor':'com-field-select',
             'options':[{'value':x.pk,'label':str(x)} for x in GameBlock.objects.all()],
             'label':'区服','required':True},
            {'name':'account','editor':'com-field-linetext',
             'label':'账号','required':True},
            {'name':'character','editor':'com-field-select','options':[],
             'mounted_express':'''scope.vc.$watch("row.account",v=>{if(v){cfg.show_load();ex.director_call("get_charecter",{account:v}).then(options=>{cfg.hide_load();if(options.length==0){cfg.toast("没有找到对应角色")}else{  scope.vc.head.options=options   }})       }     } )
             scope.vc.$watch("row.character",v=>{  if(v){ var opt = ex.findone(scope.vc.head.options,{value:v}); scope.vc.row._character_label = opt.label  }   })
             ''' ,
             'label':'角色','required':True},
        ]


@director_view('get_charecter')
def get_charecter(account):
    '''account_id='wyh99999 ''' 
    options =[]
    crt_user = get_request_cache()['request'].user
    if not GamePlayer.objects.filter(agent__account = crt_user,acount=account).exists():
        raise UserWarning('没有找到该用户')
    for inst in TbCharacter.objects.using('game_sqlserver').filter(account_id=account):
        options.append({
            'value':inst.pc_id,'label':inst.pc_name
        })
    return options


director.update({
    'recharge_mb.form':RechargeForm
})

mb_page.update({
    'home':Home
})