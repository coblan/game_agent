from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,has_permit,RowFilter
from .models import Recharge

class RechargePage(TablePage):
    def get_label(self):
        return '充值记录'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = Recharge
        exclude =[]
        
        def inn_filter(self, query):
            if has_permit(self.crt_user,'-agent_constraint'):
                query = query.filter(agent__account = self.crt_user)
            return query
        
        def get_operation(self):
            ops = super().get_operation()
            out = []
            for op in ops:
                if op['name'] == 'add_new':
                    if getattr(self.crt_user,'agentuser',None):
                        op['label'] = '充值'
                        out.append(op)
            return out
        
        class filters(RowFilter): 
            @property
            def names(self):
                names_ = ['player__acount']
                if not has_permit(self.crt_user,'-agent_constraint'):
                    names_.append('agent__name')
                return names_
            
            icontains=['player__acount','agent__name']
            range_fields =['createtime']
            def getExtraHead(self):
                return [
                    {'name':'player__acount','label':'玩家账号','editor':'com-filter-text'},
                    {'name':'agent__name','label':'代理人','editor':'com-filter-text','visible':not has_permit(self.crt_user,'-agent_constraint')},
                ]

class RechargeForm(ModelFields):
    class Meta:
        model = Recharge
        exclude =[]
        

director.update({
    'recharge':RechargePage.tableCls,
    'recharge.edit':RechargeForm,
})

page_dc.update({
    'recharge':RechargePage
})