from helpers.director.shortcut import Fields,FieldsPage,page_dc,director
from helpers.director.access.permit import has_permit
from .port_game import game_recharge
import re

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
            return ops
        
        def get_heads(self):
            return [
                {'name':'player_list','label':'接收玩家','editor':'com-field-blocktext','help_text':'以逗号，分号或者换行分割','required':True},
                {'name':'item','label':'物品','editor':'com-field-linetext','help_text':'不填写表示钻石'},
                {'name':'amount','label':'数量','editor':'com-field-int','required':True,'fv_rule':'integer(+);'},
            ]
        
        def save_form(self):
            players = re.split('[;,\n]+',self.player_list)
            for play in players:
                palyer = play.strip()
                if self.kw.get('item'):
                    game_recharge(palyer,self.kw.get('amount'),self.kw.get('item'))
                else:
                    # 钻石的时候没有item
                    game_recharge(palyer,self.kw.get('amount'),)

        

director.update({
    'batch_send':BatchSendPage.fieldsCls
})

page_dc.update({
    'batch_send':BatchSendPage,
})