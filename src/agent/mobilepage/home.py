from hello.engin_menu import mb_page
from helpers.director.shortcut import Fields,director,director_view,get_request_cache
from helpers.mobile.shortcut import FieldsMobile
from agent.game_models import TbCharacter
from agent.models import GameBlock,GamePlayer,Recharge,Game,RechargeBonus
from django.core.exceptions import PermissionDenied 

from django.utils import timezone
from django.utils.translation import ugettext as _
from agent.port_game import game_recharge

class Home(object):
    def __init__(self, request, engin):
        if not getattr(request.user,'agentuser',None):
            raise PermissionDenied(_('您不是代理人用户') )
    
    def get_template(self):
        return 'mobile/live_show.html'
    
    def get_context(self):
        return {
            'editor':'live_cell',
            'editor_ctx':  { 'title':_('代理人系统'),
                             'cells':[
                                 {'label':_('玩家充值'),
                                  'fields_ctx':{**RechargeForm().get_context(),
                                                 'after_save_express':'cfg.toast("%(recharge)s");scope.vc.row.character="";scope.vc.row.account="";scope.vc.row.recharge_amount=""'%{'recharge':_('充值成功!') },
                                                'title':_('玩家充值')},
                                  'click_express':'live_root.open_live(live_fields,scope.head.fields_ctx)',
                                  },
                                 {'label':_('新人福利'),
                                   'fields_ctx':{**NewPlayerGift().get_context(),
                                                 'after_save_express':'cfg.toast("发放成功!");scope.vc.row.character="";scope.vc.row.account="";',
                                                'title':_('新人福利')},
                                  'click_express':'live_root.open_live(live_fields,scope.head.fields_ctx)',
                                  
                                  },
                             ],
                             'bottom_editors':[
                                 {'label':_('退出登录'),
                                  'click_express':'location="/accounts/logout?next=/mb/home"','editor':'com-btn','type':'warning',
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
            {'name':'game','editor':'com-field-select','label':_('游戏'),'required':True,'options':[
                {'value':x.pk,'label':str(x)} for x in Game.objects.all()
                ]},
            {'name':'block','editor':'com-field-select',
             'options':[{'value':x.pk,'label':str(x)} for x in GameBlock.objects.all()],
             'label':_('区服'),'required':True},
            {'name':'account','editor':'com-field-linetext',
             #'mounted_express':'scope.vc.$on("blur",(e)=>{live_root.$emit("account_change",e)})',
             'label':_('账号'),'required':True},
            {'name':'character','editor':'com-field-select','options':[],
             
             'mounted_express':'''function get_character(block, account){
             scope.row.character='';
             scope.vc.options =[];
                 cfg.show_load();
                 ex.director_call("player_get_charecter",{block:block , account:account,})
                 .then(options=>{cfg.hide_load();if(options.length==0){cfg.toast("%(not_found_charactor)s")}else{  scope.vc.options=options   }})
             }
             
             scope.vc.$watch("row.account",account =>{if(scope.row.block && account  ){   get_character(scope.row.block,account )     }     } );
             scope.vc.$watch("row.block", block=>{if(block && scope.row.account ){   get_character(block,scope.row.account)     }     } );
             
             scope.vc.$watch("row.character",v=>{   if(v){ var opt = ex.findone(scope.vc.options,{value:v}); scope.vc.row._character_label = opt.label  }   })
            '''%{'not_found_charactor':_('没有找到对应角色')},
             
             #'mounted_express':'''
             #scope.vc.$watch("row.account",v=>{if(v){cfg.show_load();scope.vc.options=[];scope.row.character=''; ex.director_call("get_charecter",{account:v}).then(options=>{cfg.hide_load();if(options.length==0){cfg.toast("没有找到对应角色")}else{  scope.vc.options=options   }})       }     } )
             #scope.vc.$watch("row.character",v=>{  if(v){ var opt = ex.findone(scope.vc.options,{value:v}); scope.vc.row._character_label = opt.label  }   })
             #''' 
             
             'label':_('角色'),'required':True},
            {'name':'amount','editor':'com-field-int','label':_('当前余额'),'readonly':True},
            {'name':'recharge_amount','editor':'com-field-int','label':_('充值金额'),'required':True,'fv_rule':'integer(+)'},
        ]
    
    def dict_row(self):
        return {
            'amount':self.crt_user.agentuser.amount
        }
    
    def clean(self):
        if self.kw.get('recharge_amount') > self.kw.get('amount'):
            self.add_error('recharge_amount',_('充值金额不够') )

    
    def save_form(self):
        self.crt_user.agentuser.amount  -= self.kw.get('recharge_amount')
        if self.crt_user.agentuser.amount <0:
            raise UserWarning(_('余额不足') )
        self.crt_user.agentuser.save()
        block = GameBlock.objects.get(pk = self.kw.get('block'))
        player = GamePlayer.objects.get(acount=self.kw.get('account'),block=block )
        player.credit += self.kw.get('recharge_amount')
        player.history_credit += self.kw.get('recharge_amount')
        player.save()
        
        # 如果每天持续充值，会得到 领取奖品奖励。 实现方式:第二天去掉 30 
        record = Recharge.objects.filter( player=player,).order_by('-createtime').first()
        if record and record.createtime.date() < timezone.now().date():
            ls = player.has_get.split(',')
            if '30' in ls:
                ls.remove('30')
                player.has_get = ','.join(ls)
                player.save()

        recharg_inst = Recharge.objects.create(agent=self.crt_user.agentuser,game_id=self.kw.get('game'),
                                block=block,
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
        game_recharge(block.charge_api,self.kw.get('character'), diamond_amount )
        
        if player.par:
            # 当用户A 有上级的时候，需要给上级用户反馈30%的积分
            amount = recharg_inst.amount * 0.3
            RechargeBonus.objects.create(player=player.par,recharge = recharg_inst,
                                         amount=amount)
            player.par.credit += amount
            player.par.save()
       

class NewPlayerGift(FieldsMobile):
    
    def get_operations(self):
        ops = super().get_operations()
        for op in ops:
            if op['name']=='save':
                op['label'] = _('发放')
                #op['after_save_express'] ='cfg.hide_load();cfg.toast("发放成功")'
                #op['click_express'] = 'scope.ps.vc.ctx.after_save_express=scope.head.after_save_express; scope.ps.vc.submit()'
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
             'label':_('账号'),'required':True},
            {'name':'character','editor':'com-field-select','options':[],
             #'mounted_express':'''function get_character(block, account){
             #scope.row.character='';
             #scope.vc.options =[];
                 #cfg.show_load();
                 #ex.director_call("player_get_charecter",{block:block , account:account,})
                 #.then(options=>{cfg.hide_load();if(options.length==0){cfg.toast("没有找到对应角色")}else{  scope.vc.options=options   }})
             #}
             
             #scope.vc.$watch("row.account",account =>{if(scope.row.block && account  ){   get_character(scope.row.block,account )     }     } );
             #scope.vc.$watch("row.block", block=>{if(block && scope.row.account ){   get_character(block,scope.row.account)     }     } );
             
             #scope.vc.$watch("row.character",v=>{   if(v){ var opt = ex.findone(scope.vc.options,{value:v}); scope.vc.row._character_label = opt.label  }   })             
            #'''
            'mounted_express':'''function new_guy(account,block){
                cfg.show_load();
                scope.vc.options=[];
                scope.row.character='';
                ex.director_call("get_new_guy_gift",{account:account,block:block}).then(options=>{cfg.hide_load();if(options.length==0){cfg.toast("没有找到对应角色")}else{  scope.vc.options=options   }})
            }
            scope.vc.$watch("row.account",v=>{if(v && scope.row.block){ new_guy( v,scope.row.block )       }     } );
            scope.vc.$watch("row.block",v=>{if(v && scope.row.account){ new_guy( scope.row.account,v )       }     } );
            
            scope.vc.$watch("row.character",v=>{  if(v){ var opt = ex.findone(scope.vc.options,{value:v}); scope.vc.row._character_label = opt.label  }   })
            '''
             #'mounted_express':'''scope.vc.$watch("row.account",v=>{if(v){cfg.show_load();scope.vc.options=[];scope.row.character='';ex.director_call("get_new_guy_gift",{account:v}).then(options=>{cfg.hide_load();if(options.length==0){cfg.toast("没有找到对应角色")}else{  scope.vc.options=options   }})       }     } )
             #scope.vc.$watch("row.character",v=>{  if(v){ var opt = ex.findone(scope.vc.options,{value:v}); scope.vc.row._character_label = opt.label  }   })
             #''' 
             ,
             'label':_('角色'),'required':True},
        ]
    
    def save_form(self):
        block = GameBlock.objects.get(pk =self.kw.get('block'))
        try:
            player = GamePlayer.objects.get(acount = self.kw.get('account') ,block_id=self.kw.get('block') )
            if player.agent != self.crt_user.agentuser:
                raise UserWarning(_('该玩家不属于本代理') )
        except GamePlayer.DoesNotExist:
            player = GamePlayer.objects.create(acount = self.kw.get('account'),agent = self.crt_user.agentuser,block_id=self.kw.get('block'))
        if not player.new_guy_gift :
            player.new_guy_gift = True
            player.save()         
            game_recharge(block.charge_api,self.kw.get('character'), 20000)
            game_recharge(block.charge_api,self.kw.get('character'), 999,'getexp04')        


#@director_view('get_charecter')
#def get_charecter(account):
    #'''account_id='wyh99999 ''' 
    #options =[]
    #crt_user = get_request_cache()['request'].user
    #if not GamePlayer.objects.filter(agent__account = crt_user,acount=account).exists():
        #raise UserWarning('没有找到该用户')
    #for inst in TbCharacter.objects.using('game_sqlserver').filter(account_id=account):
        #options.append({
            #'value':inst.pc_id,'label':inst.pc_name
        #})
    #return options

@director_view('get_new_guy_gift')
def get_new_guy_gift(account,block):
    '''account_id='wyh99999 ''' 
    options =[]
    crt_user = get_request_cache()['request'].user
    
    block_inst = GameBlock.objects.get(pk = block)
    
    if not GamePlayer.objects.filter(acount=account,block = block_inst).exists():
        if not TbCharacter.objects.using(block_inst.db).filter(account_id=account).exists():
            raise UserWarning(_('没有找到角色!') )
    
    elif not GamePlayer.objects.filter(agent__account = crt_user,block = block_inst,acount=account,new_guy_gift=False).exists():
        raise UserWarning(_('该用户不属于本代理或已经领取过新人福利。') )
    for inst in TbCharacter.objects.using(block_inst.db).filter(account_id=account):
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