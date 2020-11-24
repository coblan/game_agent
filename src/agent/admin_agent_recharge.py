from helpers.director.shortcut import ModelTable,TablePage,ModelFields,director,page_dc,RowFilter
from . models import AgentRecharge
from django.db.models import Sum
from django.utils import timezone

class AgentRecharegePage(TablePage):
    def get_label(self):
        return '代理人充值'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = AgentRecharge
        exclude =['id']
        
        def dict_head(self, head):
            width ={
                'agent':150,
                'amount':150,
                'createtime':150,
            }
            if head['name'] in width:
                head['width'] = width[head['name']]
            
            return head
        
        def get_operation(self):
            ops = super().get_operation()
            out= []
            for op in ops:
                if op['name'] =='add_new':
                    op['label'] ='充值'
                    out .append(op)
            return out
        
        def statistics(self, query):
            dc = query.aggregate(amount_sum=Sum('amount'))
            self.footer={
                '_label':'合计',
                'amount':dc.get('amount_sum')}
            return query        
        
        @classmethod
        def clean_search_args(cls, search_args):
            if '_searched' not in search_args:
                now = timezone.now()
                search_args['_searched'] =1
                search_args['_start_createtime'] = now .strftime('%Y-%m-%d 00:00:00')
            return search_args        
        
        class filters(RowFilter):
            names =['agent']
            range_fields=['createtime']
        

class AgentRchageForm(ModelFields):
    #hide_fields=['admin']
    class Meta:
        model = AgentRecharge
        exclude =['admin'] 
    
    def dict_head(self, head):
        if head['name'] =='amount':
            head['fv_rule'] ='integer(+)'
        return head
    
    def clean_save(self):
        if not self.instance.admin:
            self.instance.admin = self.crt_user
    
    def after_save(self):
        if self.is_create:
            self.instance.agent.amount += self.instance.amount
            self.instance.agent.save()
    
    def dict_row(self, inst):
        if inst.admin:
            return {
                '_admin_label':str(inst.admin),
                'createtime':inst.createtime.strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            return {}
    

director.update({
    'agentrechage':AgentRecharegePage.tableCls,
    'agentrechage.edit':AgentRchageForm
})

page_dc.update({
    'agentrechage':AgentRecharegePage
})