from helpers.director.shortcut import page_dc
from .models import GamePlayer,Recharge,AgentRecharge
from django.utils import timezone
from django.db.models import Sum,Count,F
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
        new_player.reverse()
        recharge_amount.reverse()
        
        month_statistic ={
            'name':'month_static',
            'editor':'com-layout-div',
             'css':'.inline-div .div-item{display:inline-block}',
             'class':'inline-div',
             'label':'月统计',
             'items':[
                         {
                         'editor':'com-chart-general',
                         'label':'ss',
                         'name':'new_player',
                         'mounted_express':'scope.vc.draw()',
                         'rows':new_player,
                         'x':'date',
                         'y':[{'name':'count', 'color':'#27B6AC','label':'新手玩家'},# 'type':'line',
                              ],                         
                     },
                         {
                         'editor':'com-chart-general',
                         'label':'ss',
                         'name':'recharge_amount',
                         'mounted_express':'scope.vc.draw()',
                         'rows':recharge_amount ,
                         'x':'date',
                         'y':[{'name':'amount', 'label':'充值数量'}, #'type':'line',
                              ],                         
                     },
                        
                           
                     ]
                     }
        if not getattr( self.crt_user, 'agentuser',None):
            agent_rank=[]
            for instdc in Recharge.objects.filter(createtime__date__gte=month_ago.date()).annotate(agent_name=F('agent__name'))\
                .values('agent','agent_name').annotate(recharge_amout = Sum('amount') ).order_by('-recharge_amout')[:10] :
                agent_rank.append(instdc)
            
            player_rank =[]
            for instdc in Recharge.objects.filter(createtime__date__gte=month_ago.date()).annotate(player_name=F('player__acount'))\
                .values('player','player_name').annotate(recharge_amout = Sum('amount') ).order_by('-recharge_amout')[:10] :
                player_rank.append(instdc)            
            
            month_statistic['items'].extend([
                #{
                #'editor':'com-chart-horizen-type-bar',
                #'label':'代理人充值',
                #'name':'agent_recharge',
                #'class':'long-chart',
                #'css':'.long-chart .mychart{height:600px}',
                #'mounted_express':'setTimeout(()=>{ scope.vc.draw() } ,100 )',
                #'rows':recharge_amount ,
                #'x':'date',
                #'y':[{'name':'amount', 'label':'充值数量'}, #'type':'line',
                     #],                         
            #},
                {
                'editor':'com-chart-category-bar',
                'label':'代理人排名',
                'name':'agent_rank',
                'mounted_express':'scope.vc.draw()',
                'rows':agent_rank,
                'x':'agent_name',
                'y':[
                    {'name':'recharge_amout', 'color':'#27B6AC','label':'充值金额','barMaxWidth':16},
                    #{'name':'count', 'color':'#27B6AC','label':'新手玩家','barMaxWidth':20},# 'type':'line',
                    #{'name':'count1','label':'新手玩家1','barMaxWidth':10}
                                ],

             },
                {
                'editor':'com-chart-category-bar',
                'label':'玩家排名',
                'name':'player_rank',
                'mounted_express':'scope.vc.draw()',
                'rows':player_rank,
                #'class':'big1-chart',
                #'css':'.big1-chart .mychart{width:600px}',
                'option_express':'''scope.option.yAxis.axisLabel={ interval: 0,rotate: 30};
                scope.option.grid={left:"20%"}''',
                'x':'player_name',
                'y':[
                    {'name':'recharge_amout', 'label':'充值金额','barMaxWidth':16},

                 ],

             },
                
            ])
        
        return {
            'editor':'com-layout-vertical',
            'editor_ctx':{
                'items':[
                    {'name':'day_static','editor':'com-pan-static1',
                     'label':'今日统计',
                     'rows':rows
                     },
                    month_statistic
                ]
            }
        }

page_dc.update({
    'phome':MyHome
})