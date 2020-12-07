from helpers.director.shortcut import page_dc
from .models import GamePlayer,Recharge,AgentRecharge
from django.utils import timezone
from django.db.models import Sum,Count
from django.db.models.functions import TruncDate

class MyHome(object):
    
    def __init__(self, request,*args, **kwargs):
        self.crt_user = request.user
    
    def get_template(self):
        return 'jb_admin/live.html'
    
    def get_context(self):
        now = timezone.now()
        month_ago = now - timezone.timedelta(days=30)
        
        gameplay_query= GamePlayer.objects.all()
        recharge_query = Recharge.objects.all()
        if 1 in [x.pk for x  in self.crt_user.groups.all()]:
            player_count = GamePlayer.objects.filter(agent=self.crt_user.agentuser,createtime__date=now.date()).count()
            palyer_recharge_count = Recharge.objects.filter(createtime__date=now.date(),agent=self.crt_user.agentuser).values('player').count()
            total_amount = Recharge.objects.filter(createtime__date=now.date(),agent=self.crt_user.agentuser).aggregate(total_amount=Sum('amount')).get('total_amount') or 0
            
            gameplay_query = gameplay_query.filter(agent=self.crt_user.agentuser)
            recharge_query= recharge_query.filter(agent=self.crt_user.agentuser)
            
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
            
        new_player =[]
        for inst in gameplay_query.filter(createtime__date__gte=month_ago.date()).annotate(date = TruncDate('createtime')).values('date').annotate(count=Count('id')):
            new_player.append(inst)
        
        recharge_amount = []
        for inst in recharge_query.filter(createtime__date__gte=month_ago.date()).annotate(date = TruncDate('createtime')).values('date').annotate(amount=Sum('amount')):
            recharge_amount.append(inst)
        
        return {
            'editor':'com-layout-vertical',
            'editor_ctx':{
                'items':[
                    {'name':'day_static','editor':'com-pan-static1',
                     'label':'今日统计',
                     'rows':rows
                     },
                    {'name':'month_static','editor':'com-layout-div',
                     'css':'.inline-div .div-item{display:inline-block}',
                     'class':'inline-div',
                     'label':'月统计',
                     'items':[
                         {
                         'editor':'com-chart-general',
                         'label':'ss',
                         'name':'xx',
                         'mounted_express':'scope.vc.draw()',
                         'rows':new_player.reverse(),
                         'x':'date',
                         'y':[{'name':'count', 'color':'#27B6AC','label':'新手玩家'},# 'type':'line',
                              ],                         
                     },
                         {
                         'editor':'com-chart-general',
                         'label':'ss',
                         'name':'x2',
                         'mounted_express':'scope.vc.draw()',
                         'rows':recharge_amount.reverse(),
                         'x':'date',
                         'y':[{'name':'amount', 'label':'充值数量'}, #'type':'line',
                              ],                         
                               },
                     ]
                     }
                ]
            }
        }

page_dc.update({
    'phome':MyHome
})