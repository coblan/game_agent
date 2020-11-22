from hello.engin_menu import mb_page
from helpers.director.shortcut import Fields,director,director_view,get_request_cache
from helpers.mobile .shortcut import FieldsMobile
from agent.models import Game,GameBlock,GamePlayer,StoreRecord
from agent.game_models import TbCharacter
from agent.port_game import game_recharge
from helpers.func.collection.ex import findone
from helpers.case.act_log.shortcut import operation_log

class PlayerStorePage(object):
    need_login=False
    def __init__(self, request, engin):
        pass
    
    def get_template(self):
        return 'mobile/live_show.html'
    
    def get_context(self):
        return {
            'editor':'live_fields',
            'editor_ctx':  { 
                'title':'积分商城',
                **PlayerStoreForm().get_context(),
                     }
            
            }

class PlayerStoreForm(FieldsMobile):
    nolimit = True
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
             'mounted_express':'''scope.vc.$watch("row.account",v=>{if(v){cfg.show_load();ex.director_call("player_get_charecter",{account:v}).then(options=>{cfg.hide_load();if(options.length==0){cfg.toast("没有找到对应角色")}else{  scope.vc.options=options   }})       }     } )
             scope.vc.$watch("row.character",v=>{  if(v){ var opt = ex.findone(scope.vc.options,{value:v}); scope.vc.row._character_label = opt.label  }   })
             ''' ,
             'label':'角色','required':True},
            {'name':'kind','label':'商品种类','editor':'com-field-select','required':True,
             'options':[
                {'value':x.get('value'),'label':x.get('label')} for x in store_menu
                ]},
            {'name':'product','label':'商品',
             'editor':'com-field-select','required':True,
             'options':[],
             'store_menu':store_menu,
             'mounted_express':'''scope.vc.$watch("row.kind",v=>{
             
                 var ss =ex.findone( scope.head.store_menu ,{value:v})
                 if(ss){
                     scope.vc.options = ss.items
                 }else{
                     scope.vc.options=[]
                 }
                 scope.row.product=''
                 
             })'''},
            
            #{'name':'content','label':'奖励内容','editor':'com-field-blocktext','readonly':True,
             #'mounted_express':'scope.vc.$watch("row.credit",v=>{Vue.set(scope.row,"content",scope.head.label_option[v])})',
             #'label_option':{x['value']: x['label']  for x in credit_bonus} }
        ]
    
    def clean(self):
        self.player = GamePlayer.objects.get(acount = self.kw.get('account') )
        self.kind_inst = findone(store_menu,{'value': self.kw.get('kind')} )
        self.product = findone(self.kind_inst.get('items'),{'value':self.kw.get('product')})
        
        if self.player.credit < self.kind_inst.get('credit' ) : #  self.kw.get('credit'):
            self.add_error('credit','您的积分不够,当前:%s'%self.player.credit)

    def save_form(self):

        self.player.credit -= self.kind_inst.get('credit' ) #  self.product.get('amount')
        self.player.save()
        game_recharge(self.kw.get('character'),self.product.get('amount'), self.product.get('value'))
        operation_log('用户%(account)s为其角色%(character)s提取物品%(product)s'%self.kw)
        StoreRecord.objects.create(player = self.player,
                                   credit = self.kind_inst.get('credit' ),
                                   character= self.kw.get('character'),
                                   code= self.product.get('value'))
        
        #self.player.has_get_list.append(self.kw.get('credit'))
        #self.player.has_get = ','.join( [str(x) for x in self.player.has_get_list] )
        #self.player.save()

        #for item in credit_bonus:
            #if item.get('value') ==self.kw.get('credit'):
                #content = item.get('content')
        #for k,v in content.items():
            #game_recharge(self.kw.get('character'), v,k)
            

store_menu=[
    {'value':1,'label':'职业指定紫色秘籍(1000积分)','credit':1000,'items':[
        {'value':'skb10009','label':'风火轮2段','amount':1},
        {'value':'skb10012','label':'天雷令2段','amount':1},
        {'value':'skb10014','label':'天隙流光2段','amount':1},
        {'value':'skb20015','label':'狂风3段','amount':1},
        {'value':'skb20011','label':'憾地3段','amount':1},
        {'value':'skb20017','label':'灭绝2段','amount':1},
        {'value':'skb30006','label':'炎龙啸2段','amount':1},
        {'value':'skb30010','label':'寒冰之体2段','amount':1},
        {'value':'skb30015','label':'火炎掌3段','amount':1},
        {'value':'skb10016','label':'飞燕剑3段','amount':1},
        {'value':'skb30018','label':'炎龙破3段','amount':1},
        {'value':'skb80019','label':'掠风3段','amount':1},
        {'value':'skb80021','label':'四连斩3段','amount':1},
        {'value':'skb80014','label':'风月破3段','amount':1},
    ]},
    {'value':2,'label':'职业指定橙装道具(2000积分)','credit':2000,'items':[
        {'value':'ewe51011','label':'泰山系列剑士','amount':1},
        {'value':'ewe54011','label':'泰山系列拳师','amount':1},
        {'value':'ewe53011','label':'泰山系列气功','amount':1},
        {'value':'ewe45111','label':'泰山系列刺客','amount':1},
        {'value':'ewe52011','label':'泰山系列力士','amount':1},
        {'value':'ewe56011','label':'泰山系列召唤','amount':1},
        {'value':'ewe57011','label':'泰山系列灵剑','amount':1},
        {'value':'eea50012','label':'孟川耳环','amount':1},
        {'value':'ene50012','label':'孟川项链','amount':1},
        {'value':'eri50012','label':'孟川戒指','amount':1},
        {'value':'ebr50012','label':'孟川手镯','amount':1},
        {'value':'ebe50012','label':'孟川腰带','amount':1}
    ]},
    {'value':3,'label':'职业橙宠道具(300积分)','credit':300,'items':[
        {'value':'epe10051','label':'猫头鹰','amount':1},
        {'value':'epe10052','label':'神龙','amount':1},
        {'value':'epe10061','label':'孙悟空','amount':1},
        {'value':'epe10063','label':'金鱼王','amount':1}
    ]},
    {'value':4,'label':'消耗材料(200积分)','credit':200,'items':[
        {'value':'sell0009','label':'银币袋子(数量500)','amount':500,},
        {'value':'pac10024','label':'武器强化材料包(数量200)','amount':200},
        {'value':'pac10025','label':'首饰强化材料包(数量200)','amount':200},
        {'value':'box00003','label':'上乘武功精气(数量200)','amount':20},
        {'value':'box00013','label':'上乘内功精气(数量200)','amount':20},
        {'value':'ess20003','label':'最高级青蓝精气(蓝色)数量100','amount':10},
        {'value':'ess10003','label':'最高级赤红精气(红色)数量100','amount':10},
        {'value':'ess00003','label':'最高级洪门精气(黄色)数量100','amount':10},
        {'value':'getexp04','label':'最上级经验药水(数量999)','amount':999}
        
    ]}
]


#@director_view('player_get_charecter')
#def player_get_charecter(account):
    #'''account_id='wyh99999 ''' 
    #options =[]
    #try:
        #GamePlayer.objects.get(acount = account)
    #except GamePlayer.DoesNotExist:
        #raise UserWarning('账号不存在')
    #for inst in TbCharacter.objects.using('game_sqlserver').filter(account_id=account):
        #options.append({
            #'value':inst.pc_id,'label':inst.pc_name
        #})
    #return options
    
director.update({
    'palystore_form':PlayerStoreForm,
})


mb_page.update({
    'store':PlayerStorePage
})