from hello.engin_menu import mb_page
from helpers.director.shortcut import Fields,director,director_view,get_request_cache
from helpers.mobile.shortcut import FieldsMobile
from agent.game_models import TbCharacter
from agent.models import GameBlock,GamePlayer,Recharge,Game
from django.core.exceptions import PermissionDenied 
from agent.port_game import game_recharge
from django.utils import timezone

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
                                  'fields_ctx':{**RechargeForm().get_context(),
                                                 'after_save_express':'cfg.toast("充值成功!");scope.vc.row.character="";scope.vc.row.account="";scope.vc.row.recharge_amount=""',
                                                'title':'玩家充值'},
                                  'click_express':'live_root.open_live(live_fields,scope.head.fields_ctx)',
                                  },
                                 {'label':'新人福利',
                                   'fields_ctx':{**NewPlayerGift().get_context(),
                                                 'after_save_express':'cfg.toast("发放成功!");scope.vc.row.character="";scope.vc.row.account="";',
                                                'title':'新人福利'},
                                  'click_express':'live_root.open_live(live_fields,scope.head.fields_ctx)',
                                  
                                  },
                             ],
                             'bottom_editors':[
                                 {'label':'退出登录','click_express':'location="/accounts/logout?next=/mb/home"','editor':'com-btn','type':'warning',
                                  'css':'.logout-btn{width: 74%;margin: 13%;margin-top: 1rem}','class':"logout-btn"}
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
             'mounted_express':'''scope.vc.$watch("row.account",v=>{if(v){cfg.show_load();scope.vc.options=[];scope.row.character=''; ex.director_call("get_charecter",{account:v}).then(options=>{cfg.hide_load();if(options.length==0){cfg.toast("没有找到对应角色")}else{  scope.vc.options=options   }})       }     } )
             scope.vc.$watch("row.character",v=>{  if(v){ var opt = ex.findone(scope.vc.options,{value:v}); scope.vc.row._character_label = opt.label  }   })
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
        player.credit += self.kw.get('recharge_amount')
        player.history_credit += self.kw.get('recharge_amount')
        player.save()
        
        record = Recharge.objects.filter( player=player,).order_by('-createtime').first()
        if record and record.createtime.date() < timezone.now().date():
            ls = player.has_get.split(',')
            if '30' in ls:
                ls.remove('30')
                player.has_get = ','.join(ls)
                player.save()

        Recharge.objects.create(agent=self.crt_user.agentuser,game_id=self.kw.get('game'),
                                block_id=self.kw.get('block'),
                                player=player,
                                charactar=self.kw.get('_character_label'),
                                pc_id=self.kw.get('character'),
                                amount=self.kw.get('recharge_amount'),
                                status=1)
        if record:
            mutiple = 300
        else:
            mutiple = 600
            
        diamond_amount = self.kw.get('recharge_amount') * mutiple
        game_recharge(self.kw.get('character'), diamond_amount )
       

class NewPlayerGift(FieldsMobile):
    
    def get_operations(self):
        ops = super().get_operations()
        for op in ops:
            if op['name']=='save':
                op['label'] = '发放'
                #op['after_save_express'] ='cfg.hide_load();cfg.toast("发放成功")'
                #op['click_express'] = 'scope.ps.vc.ctx.after_save_express=scope.head.after_save_express; scope.ps.vc.submit()'
        return ops
    
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
             'mounted_express':'''scope.vc.$watch("row.account",v=>{if(v){cfg.show_load();scope.vc.options=[];scope.row.character='';ex.director_call("get_new_guy_gift",{account:v}).then(options=>{cfg.hide_load();if(options.length==0){cfg.toast("没有找到对应角色")}else{  scope.vc.options=options   }})       }     } )
             scope.vc.$watch("row.character",v=>{  if(v){ var opt = ex.findone(scope.vc.options,{value:v}); scope.vc.row._character_label = opt.label  }   })
             ''' ,
             'label':'角色','required':True},
        ]
    
    def save_form(self):
        try:
            player = GamePlayer.objects.get(acount = self.kw.get('account'))
            if player.agent != self.crt_user.agentuser:
                raise UserWarning('该玩家不属于本代理')
        except GamePlayer.DoesNotExist:
            player = GamePlayer.objects.create(acount = self.kw.get('account'),agent = self.crt_user.agentuser)
        if not player.new_guy_gift :
            player.new_guy_gift = True
            player.save()         
            game_recharge(self.kw.get('character'), 20000)
            game_recharge(self.kw.get('character'), 999,'getexp04')        


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

@director_view('get_new_guy_gift')
def get_new_guy_gift(account):
    '''account_id='wyh99999 ''' 
    options =[]
    crt_user = get_request_cache()['request'].user
    
    
    if not GamePlayer.objects.filter(acount=account).exists():
        if not TbCharacter.objects.using('game_sqlserver').filter(account_id=account).exists():
            raise UserWarning('没有找到角色!')
    
    elif not GamePlayer.objects.filter(agent__account = crt_user,acount=account,new_guy_gift=False).exists():
        raise UserWarning('该用户不属于本代理或已经领取过新人福利。')
    for inst in TbCharacter.objects.using('game_sqlserver').filter(account_id=account):
        options.append({
            'value':inst.pc_id,'label':inst.pc_name
        })
    return options

director.update({
    'recharge_mb.form':RechargeForm,
    'recharge_mb.new_guy_gift':NewPlayerGift,
})

mb_page.update({
    'home':Home
})