from hello.engin_menu import mb_page
from helpers.director.shortcut import Fields,director,director_view,get_request_cache
from helpers.mobile .shortcut import FieldsMobile
from agent.models import Game,GameBlock,GamePlayer
from agent.game_models import TbCharacter
from agent.port_game import game_recharge
from django.conf import settings
from django.utils.translation import ugettext as _

class PlayerCredit(object):
    need_login=False
    def __init__(self, request, engin):
        pass
    
    def get_template(self):
        return 'mobile/live_show.html'
    
    def get_context(self):
        return {
            'editor':'live_fields',
            'editor_ctx':  { 
                'title':_('累计充值奖励'),
                **CreditForm().get_context(),
                     }
            
            }

class CreditForm(FieldsMobile):
    nolimit = True
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
             '''%{'not_found_charactor':_("没有找到对应角色")} ,
             'label':_('角色'),'required':True},
            {'name':'history_credit','label':_('累积积分'),'editor':'com-field-select','required':True,
             'options':[{'value':x['value'],'label':x['text']} for x in credit_bonus]},
            {'name':'content','label':_('奖励内容'),'editor':'com-field-blocktext','readonly':True,
             'mounted_express':'scope.vc.$watch("row.history_credit",v=>{Vue.set(scope.row,"content",scope.head.label_option[v])})',
             'label_option':{x['value']: x['label']  for x in credit_bonus} }
        ]
    
    def clean(self):
        self.block = GameBlock.objects.get(pk = self.kw.get('block'))
        self.player = GamePlayer.objects.get(acount = self.kw.get('account') ,block= self.block )
        if self.player.history_credit <  self.kw.get('history_credit'):
            self.add_error('history_credit',_('您的累积积分不够,当前:%s')%self.player.history_credit)
        ls = [x for x in self.player.has_get.split(',') if x]
        self.player.has_get_list = ls
        if str( self.kw.get('history_credit') ) in self.player.has_get_list:
            self.add_error('history_credit',_('您已经领取过了该积分段奖品'))
            
    def save_form(self):
        # 30 已经的只能领一次
   
        self.player.has_get_list.append(self.kw.get('history_credit'))
        self.player.has_get = ','.join( [str(x) for x in self.player.has_get_list] )
        self.player.save()

        for item in credit_bonus:
            if item.get('value') ==self.kw.get('history_credit'):
                content = item.get('content')
        for k,v in content.items():
            game_recharge(self.block.charge_api,self.kw.get('character'), v,k)
            

credit_bonus=[
    {'value':30,'text':'累积充值30元','label':'钻石3000+强化材料包*10+银币袋子*5+武功精髓*5+内功精髓*5',
     'content':{'diamond':3000,'pac10024':10,'pac10025':10,'sell0009':5,'box00002':5,'box00012':5}},
    {'value':100,'text':'累积充值100元','label':'耀眼紫色武器一把+最大型银币袋子（500000）*10+泳装*1',
     'content':{"boxwe410":1 ,"sell0009":10, "mou00032": 1}},
    {'value':300,'text':'累积充值300元','label':'天命剑紫色武器图纸*1+强化材料礼包*50+负重卷轴+1000*10 最大型银币袋子（500000）*20+经验成长水*100',
     'content':{'sbimu001':1 , "pac10024":50, "pac10025" :50 , "wei40011":10 , "sell0009" : 20 , "getexp04": 100}},
    {'value':500,'text':'累积充值500元','label':'橙色武器图纸*1+传奇图案箱子*100武器强化石礼包*100+ 首饰强化礼包*100+ 最大型银币袋子（500000）*100+经验成长水*999+负重*10+随机紫时装图纸*1+顶级武器材料*50+高级金属*200+特殊金属*90',
     'content':{"all00001":1 , "all00005" :100 , "pac10025" : 100 , "pac10024" : 100 , "wei40011" : 10 , "sell0009" : 60 , "getexp04": 999,
                "box83003":1,"cre00502" :50 ,"cre10002":200,"cre10003":80}
     },
    {'value':1000,'text':'累积充值1000元','label':'橙色武器图纸*1+传奇图案箱子*300 强化材料*100+ 负重卷轴+1000 *10+最大型银币袋子（500000）*100+（大武功精髓+大内功精髓各自50个）+经验成长水*999*2+顶级制作材料箱子*100',
     'content':{"all00001":1 , "all00005" : 300 , "pac10024" : 100 , "pac10025" :100 , "wei40011" : 10 , "sell0009" : 100 , "box00003" : 50 , "box00013" :50 , "getexp04" : 1998 , "bem10425": 100}},
    {'value':2000,'text':'累积充值2000元','label':'武神戒指*2+强化材料*100+ 负重卷轴+1000 *10+最大型银币袋子（500000）*100+（大武功精髓+大内功精髓各自70个）+经验成长水*999*2+武器修复舱*5+首饰修复舱*5+随机橙时装图纸*1+固定精炼石*9999',
     'content':{"eri50011":2 , "pac10024" : 100 , "pac10025" : 100 , "wei40011" : 10 , "sell0009":100 , "box00003" :70 , "box00013" :70 , "getexp04" : 1998 , "rst50003" :5, "rst50103" :5 , "box83004" : 1, "ref10002" :9999}},
    {'value':3000,'text':'累积充值3000元','label':'武神手镯*2+强化材料*100+ 负重卷轴+1000 *10+最大型银币袋子（500000）*100+（大武功精髓+大内功精髓各自100个）+经验成长水*999*2+武器修复舱*10+首饰修复舱*10+固定精炼石*9999+再精炼石*9999',
     'content':{"ebr50011": 2 , "pac10024" : 100 , "pac10025" : 100 , "wei40011" : 10 , "sell0009" :100 , "box00003" :100 , "box00013" :100 , "getexp04" :1998 , "rst50003": 10, "rst50103" : 10 , "ref10002" : 9999 , "ref10001" :9999}},
    {'value':4000,'text':'累积充值4000元','label':'武神耳环*2+强化材料*100+ 负重卷轴+1000 *10+最大型银币袋子（500000）*100+（大武功精髓+大内功精髓各自120个）+经验成长水*999*2+武器修复舱*15+首饰修复舱*15+固定精炼石*9999+再精炼石*9999',
     'content':{"eea50011": 2 , "pac10024" : 100 , "pac10025" : 100 , "wei40011" : 10 , "sell0009" : 100 , "box00003" : 120 , "box00013" :120 , "getexp04" : 1998 , "rst50003" :15 , "rst50103" :15 ,"ref10002" :9999 , "ref10001" :9999}},
    {'value':5000,'text':'累积充值5000元','label':'武神腰带*1+武神项链*1+强化材料*100+ 负重卷轴+1000 *10+最大型银币袋子（500000）*200+（大武功精髓+大内功精髓各自200个）+经验成长水*999*5+武器修复舱*20+首饰修复舱*20+橙装箱子*5',
     'content':{"ene50011" : 1 , "ebe50011" : 1 ,  "pac10024" :100 , "pac10025" :100 , "wei40011" :10 , "sell0009" :200 , "box00003" :200 , "box00013" :200 , "getexp04" : 4995 , "rst50003" :20 , "rst50103" :20, "all00005" :5}},
    {'value':8000,'text':'累积充值8000元','label':'橙首饰一套+橙宠神龙*1+固定精炼石*9999+再燃石*9999+武器修复舱*50+首饰修复舱*50+大武功精髓+大内功精髓各自200个+最高级青蓝精气(蓝色)*100+最高级赤红精气（红色）*100+最高级洪门精气（黄色）*100+经验水999*10',
     'content':{"eea50011" :1 , "ene50011" : 1 , "eri50011" :1 , "ebr50011" :1 ,"ebe50011" :1 , "epe10052" :1 , "ref10001" :9999 , "ref10002": 9999 , "rst50003" :50 , "rst50103" : 50 , "box00003" : 200 , "box00013" :200 , "ess20003" : 100 , "ess10003" :100 , "ess00003" : 100 , "getexp04" :9990}}
]


@director_view('player_get_charecter')
def player_get_charecter(block,account):
    '''account_id='wyh99999 ''' 
    options =[]
    block_inst = GameBlock.objects.get(pk = block)
    try:
        GamePlayer.objects.get(acount = account,block=block_inst)
    except GamePlayer.DoesNotExist:
        raise UserWarning('账号不存在')
    for inst in TbCharacter.objects.using(block_inst.db).filter(account_id=account):
        options.append({
            'value':inst.pc_id,'label':inst.pc_name
        })
    return options
    
director.update({
    'playercredit':CreditForm,
})


mb_page.update({
    'player':PlayerCredit
})