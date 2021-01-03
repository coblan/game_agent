from helpers.director.shortcut import Fields,FieldsPage,page_dc,director
from helpers.director.access.permit import has_permit
from .port_game import game_recharge
import re
from agent.models import GameBlock

class BatchSendPage(FieldsPage):
    def get_label(self):
        return '批量发放'
    
    def check_permit(self):
        return has_permit(self.request.user,'batch_send')
    
    def get_template(self, prefer=None):
        return 'jb_admin/fields.html'
    
    class fieldsCls(Fields): 
        
        def get_operations(self):
            ops = super().get_operations()
            for op in ops:
                op['label']= '发放'
                op['click_express'] = 'cfg.confirm("确认填写正确，发放物品?").then(()=>{return scope.ps.vc.submit()}).then(()=>{scope.ps.vc.row.is_all_player=false;scope.ps.vc.row.player_list="";scope.ps.vc.row.amount=""})'
            return ops
        
        def get_heads(self):
            return [
                {'name':'is_all_player','label':'全体玩家','editor':'com-field-bool'},
                {'name':'block','label':'游戏分区','required':True,'editor':'com-field-select','options':[
                    {'value':x.pk,'label':x.name} for x in GameBlock.objects.all()
                    ]},
                {'name':'player_list','label':'接收玩家',
                 'show_express':'rt=!scope.row.is_all_player',
                 'editor':'com-field-blocktext','required':True,
                 'help_text':'以逗号，分号或者换行分割;',},
                {'name':'item','label':'物品','editor':'com-field-linetext','help_text':'不填写表示钻石'},
                {'name':'amount','label':'数量','editor':'com-field-int','required':True,'fv_rule':'integer(+);'},
            ]
        
        def save_form(self):
            block = GameBlock.objects.get(pk = self.kw.get('block'))
            if self.kw.get('is_all_player'):
                palyer = None
                if self.kw.get('item'):
                    game_recharge(block.charge_api,palyer,self.kw.get('amount'),self.kw.get('item'))
                else:
                    # 钻石的时候没有item
                    game_recharge(block.charge_api,palyer,self.kw.get('amount'),)
            elif self.kw.get('player_list'):
                players = re.split('[;,\n]+',self.kw.get('player_list'))
                for play in players:
                    palyer = play.strip()
                    if self.kw.get('item'):
                        game_recharge(block.charge_api,palyer,self.kw.get('amount'),self.kw.get('item'))
                    else:
                        # 钻石的时候没有item
                        game_recharge(block.charge_api,palyer,self.kw.get('amount'),)
     
               

        

director.update({
    'batch_send':BatchSendPage.fieldsCls
})

page_dc.update({
    'batch_send':BatchSendPage,
})