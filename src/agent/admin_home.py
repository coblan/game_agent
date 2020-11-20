from helpers.director.shortcut import page_dc
from .models import GamePlayer,Recharge,AgentRecharge
from django.utils import timezone
from django.db.models import Sum

class MyHome(object):
    
    def __init__(self, request,*args, **kwargs):
        self.crt_user = request.user
    
    def get_template(self):
        return 'jb_admin/live.html'
    
    def get_context(self):
        now = timezone.now()
        if 1 in [x.pk for x  in self.crt_user.groups.all()]:
            player_count = GamePlayer.objects.filter(agent=self.crt_user.agentuser,createtime__date=now.date()).count()
            palyer_recharge_count = Recharge.objects.filter(createtime__date=now.date(),agent=self.crt_user.agentuser).values('player').count()
            total_amount = Recharge.objects.filter(createtime__date=now.date(),agent=self.crt_user.agentuser).aggregate(total_amount=Sum('amount')).get('total_amount') or 0
        
            rows =[
              {'label':'新增玩家','value':player_count} , 
              {'label':'充值玩家数','value':palyer_recharge_count} ,   
              {'label':'玩家充值金额','value':total_amount} ,   
              ]
        else:
            player_count = GamePlayer.objects.filter(createtime__date=now.date()).count()
            palyer_recharge_count = Recharge.objects.filter(createtime__date=now.date()).values('player').count()
            total_amount = Recharge.objects.filter(createtime__date=now.date()).aggregate(total_amount=Sum('amount')).get('total_amount') or 0
            agent_amount = AgentRecharge.objects.filter(createtime__date=now.date()).aggregate(total_amount=Sum('amount')).get('total_amount') or 0
            rows =[
                {'label':'新增玩家','value':player_count} , 
                {'label':'充值玩家数','value':palyer_recharge_count} ,   
                {'label':'玩家充值金额','value':total_amount} ,   
                {'label':'代理充值金额','value':agent_amount},
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