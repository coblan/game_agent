from hello.engin_menu import mb_page
from helpers.director.shortcut import Fields,director
from helpers.mobile.shortcut import FieldsMobile
class Home(object):
    def __init__(self, request, engin):
        pass
    
    def get_template(self):
        return 'mobile/live_show.html'
    
    def get_context(self):
        return {
            'editor':'live_fields',
            'editor_ctx':  { 'title':'充值',
                             #'back_action':'location="/mb/index"',
                             'after_save':'cfg.toast("发布成功!");setTimeout(()=>{history.back()},1500)',
                             **RechargeForm().get_context() 
                           }
        }
    

class RechargeForm(FieldsMobile):
    def get_heads(self):
        return [
            {'name':'ss','editor':'com-field-linetext','label':'区服','required':True},
            {'name':'ss','editor':'com-field-select','options':[],'label':'账号','required':True},
            {'name':'ss','editor':'com-field-select','options':[],'label':'角色','required':True},
            {'name':'ss','editor':'com-field-select','options':[],'label':'充值金额','required':True},
        ]
    

director.update({
    'recharge_mb.form':RechargeForm
})

mb_page.update({
    'home':Home
})