from helpers.director.shortcut import page_dc
from .models import GamePlayer,Recharge
from django.utils import timezone
from django.db.models import Sum

class MyHome(object):
    
    def __init__(self, *args, **kwargs):
        pass
    
    def get_template(self):
        return 'jb_admin/live.html'
    
    def get_context(self):
        now = timezone.now()
        player_count = GamePlayer.objects.filter(createtime__date=now.date()).count()
        palyer_recharge_count = Recharge.objects.filter(createtime__date=now.date()).values('player').count()
        total_amount = Recharge.objects.filter(createtime__date=now.date()).aggregate(total_amount=Sum('amount')).get('total_amount') or 0
        
        rows =[
            {'label':'新增用户','value':player_count} , 
            {'label':'充值用户','value':palyer_recharge_count} ,   
            {'label':'充值金额','value':total_amount} ,   
            
            ]
        #for row in rows:
            #if row.get('value') ==0:
                #row.pop('action')
        
        return {
            'editor':'com-layout-vertical',
            'editor_ctx':{
                'items':[
                    {'name':'day_static','editor':'com-pan-static1',
                     'label':'今日统计',
                     'rows':rows
                     },
                ]
            }
        }

page_dc.update({
    'phome':MyHome
})