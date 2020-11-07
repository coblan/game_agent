from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,director_save_row
from .models import AgentUser
from helpers.case.jb_admin.admin_user import UserPage,UserFields,Group
from django.utils import timezone

class AgentUserPage(TablePage):
    def get_label(self):
        return '代理人管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = AgentUser
        exclude =['id']
        pop_edit_fields = ['name']
        
        def dict_row(self, inst):
            return {
                'username':inst.account.username,
                'is_active':inst.account.is_active,
            }
        
        def dict_head(self, head):
            width = {
                'name':150,
                'account':150
            }
            if head['name'] in width:
                head['width'] = width[head['name']]
            return head
        

class AgentAcount(UserFields):
    hide_fields =['first_name','is_staff','is_superuser','email','groups','date_joined']

class AgentUserForm(ModelFields):
    #hide_fields=['account']
    class Meta:
        model = AgentUser
        exclude =['id','account']
    
    def getExtraHeads(self):
        return AgentAcount().get_heads()
    
    def dict_row(self, inst):
        if self.is_create and not inst.pk: 
            return {
                'is_active':True,
            }            
        else:
            inst.account.refresh_from_db()
            return {
                'username':inst.account.username,
                'is_active':inst.account.is_active, 
                'account':inst.account.pk,
                '_account_label':str(inst.account),
            }
        
    def clean(self):
        if not  self.is_create:
            account = self.instance.account.pk
        else:
            account = None
        account_row = {
            '_director_name':UserFields.get_director_name(),
            'username':self.kw.get('username'),
            'is_active':self.kw.get('is_active'),
            'user_password':self.kw.get('user_password'),
            'date_joined':timezone.now(),
            'is_staff':True,
            'pk':account
        }
        obj = UserFields(account_row)
        if obj.is_valid():
            obj.save_form()
            if  self.is_create:
                self.instance.account = obj.instance  
                agent_group = Group.objects.get(pk =1 )
                obj.instance.groups.add(agent_group)
        else:
            error =obj.get_errors()
            self._errors.update(error)
            #for k,v in error.items():
                #self.add_error( k,v )        
      
  
director.update({
    'agentuser':AgentUserPage.tableCls,
    'agentuser.edit':AgentUserForm,
})        
        
page_dc.update({
    'agentuser':AgentUserPage
})