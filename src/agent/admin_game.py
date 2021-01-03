from helpers.director.shortcut import TablePage, ModelTable,ModelFields,ModelTable,page_dc,director
from . models import Game,GameBlock
from django.db.models import Count

class GamePage(TablePage):
    def get_label(self):
        return '游戏管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    def get_context(self):
        ctx = super().get_context()
        ctx['named_ctx'] = {
            'game-tab':[
                {
                    'name':'game_info',
                    'label':'基本信息',
                    'editor':'com-tab-form',
                    'mounted_express':'ex.vueAssign(scope.row,scope.par_row)',
                    'fields_ctx':GameForm().get_head_context(),
                    },
                {'name':'block',
                 'label':'大区',
                 'editor':'com-tab-table',
                 'filter_express':'rt={game:scope.ps.vc.par_row.pk}',
                 'table_ctx':GameBlockTab().get_head_context()}
            ]
        }
        return ctx
    
    class tableCls(ModelTable):
        model =Game
        exclude =['id']
        
        def inn_filter(self, query):
            return query.annotate(block_count=Count('gameblock'))
        
        def dict_head(self, head):
            width = {
                'name':200,
            }
            if head['name'] in width:
                head['width'] = width[head['name']]
            if head['name'] =='name':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name'] = 'game_info'
                head['ctx_name'] = 'game-tab'
            return head
        
        def getExtraHead(self):
            return [
                {'name':'block_count','label':'大区数','editor':'com-table-span',}
            ]
        
        def dict_row(self, inst):
            return {
                'block_count':inst.block_count
            }
        
        

class GameForm(ModelFields):
    readonly =['name']
    class Meta:
        model = Game
        exclude =[] 
    
    def dict_row(self, inst):
        return {
            'block_count':inst.gameblock_set.count()
        }
    
    #def get_operations(self):
        #return []


class GameBlockTab(ModelTable):
    model = GameBlock
    exclude =['id']
    hide_fields =['game','charge_api']
    
    def dict_head(self, head):
        width = {
            'name':200,
        }
        if head['name'] in width:
            head['width'] = width[head['name']]
        return head
    
    def get_operation(self):
        ops = super().get_operation()
        for op in ops:
            if op['name'] == 'add_new':
                op['preset_express'] = 'rt={game_id:scope.ps.vc.par_row.pk}'
                op['after_save_express'] =' ex.refresh_row(scope.ps.vc.par_row)'
        return ops
    
    def inn_filter(self, query):
        return query.filter(game=self.search_args.get('game'))

class GameBlockForm(ModelFields):
    hide_fields = ['game']
    
    class Meta:
        model = GameBlock
        exclude =[]


director.update({
    'game':GamePage.tableCls,
    #'game.edit':GameForm,
    'gameBlock':GameBlockTab,
    #'gameBlock.edit':GameBlockForm,
})

page_dc.update({
    'game':GamePage
})