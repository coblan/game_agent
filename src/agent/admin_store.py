from helpers.director.shortcut import TablePage,ModelTable,RowFilter,page_dc,director
from .models  import StoreRecord

class StoreRecordPage(TablePage):
    def get_label(self):
        return '积分商城记录'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = StoreRecord
        exclude =[]
        
        class filters(RowFilter):
            names=['player__acount']
            icontains = ['player__acount']
            range_fields = ['createtime']
            
            def getExtraHead(self):
                return [
                    {'name':'player__acount','label':'玩家',}
                ]

director.update({
    'admin_store':StoreRecordPage.tableCls,
})

page_dc.update({
    'admin_store':StoreRecordPage
})