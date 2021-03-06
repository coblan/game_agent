from helpers.director.shortcut import TablePage,ModelTable,ModelFields,director,page_dc,has_permit,RowFilter,RowSort
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
        
        def inn_filter(self, query):
            if has_permit(self.crt_user,'-agent_constraint'):
                query = query.filter(agent__account=self.crt_user)
            return query
        
        def get_head_context(self):
            ctx = super().get_head_context()
            heads_names = [head['name'] for head in ctx.get('heads')]
            ctx.update({
                'advise_heads':heads_names,
            })
            return ctx        
        
        def get_operation(self):
            ops = super().get_operation()
            ops += [
                {'editor':'com-btn',
                 'label':'显示列',
                 'icon':'el-icon-s-tools',
                 'action':'cfg.pop_vue_com("com-panel-table-setting",{table_ps:scope.ps,title:"设置列"})'},
            ]
            return ops
        
        def dict_head(self, head):
            width ={
                'acount':200,
                'agent':200,
                'desp':200,
            }
            if head['name'] in width:
                head['width'] = width[head['name']]
            return head
        
        class filters(RowFilter):
            names = ['acount','agent__name']
            icontains = ['acount','agent__name']
            fields_sort=['acount','agent__name']
            def getExtraHead(self):
                return [
                    {'name':'agent__name','label':'代理人','editor':'com-filter-text','visible':not has_permit(self.crt_user,'-agent_constraint')},

                ]
        
        class sort(RowSort):
            names = ['credit','history_credit']

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
