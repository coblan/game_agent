from helpers.director.shortcut import TablePage,ModelTable,ModelFields,director,page_dc
from .models import GamePlayer

class PlayerPage(TablePage):
    def get_label(self):
        return '玩家管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = GamePlayer
        exclude =['id']
        pop_edit_fields = ['acount']
        
        def dict_head(self, head):
            width ={
                'acount':200,
                'agent':200,
            }
            if head['name'] in width:
                head['width'] = width[head['name']]
            return head

class PlayerForm(ModelFields):
    class Meta:
        model = GamePlayer
        exclude =['id']

director.update({
    'player':PlayerPage.tableCls,
    'player.edit':PlayerForm,
})

page_dc.update({
    'player':PlayerPage
})
