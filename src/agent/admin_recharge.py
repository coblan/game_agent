from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from .models import Recharge

class RechargePage(TablePage):
    def get_label(self):
        return '充值记录'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = Recharge
        exclude =[]

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