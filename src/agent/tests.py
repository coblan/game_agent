from unittest import mock
from django.test import TestCase,Client
from .models import Game,GameBlock,GamePlayer,AgentUser,EverdaySign
from django.core.management import call_command
from django.contrib.auth.models import User

# Create your tests here.
from agent.game_utile import check_account_exist
import json
from django.utils import timezone
#from agent.port_game import game_recharge

class TestSimpleWash(TestCase):
      
    def setUp(self):
        call_command('init_db')
        call_command('update_game')
        self.mock()
        
    def mock(self):
        #self.game_recharger = mock.patch('agent.port_game.game_recharge')
        self.game_recharger = mock.patch('agent.mobilepage.home.game_recharge')
        def func1(charge_api,id_N=None,qty=None,pwd_P=None,*args,**kwsg):
            print('调用游戏平台发放物品')
        self.ss = self.game_recharger.start()
        self.ss.side_effect = func1
        
        self.now_pather = mock.patch('django.utils.timezone.now')
        self.mock_now = self.now_pather.start()
        self.mock_now.return_value  = timezone.datetime.strptime('2020-01-01 10:10:10.664309','%Y-%m-%d %H:%M:%S.%f')          
        
    def test_recharge(self):
        cl = Client(enforce_csrf_checks=True)
        user = User.objects.create_user(username='testuser', password='12345')
        user.groups.add(1)
        agent1 = AgentUser.objects.create(name='代理人一',account=user,amount=5000)
        
        cl.login(username='testuser', password='12345')
        
        # 测试玩家充值与bonus逻辑
        #=============================
        player1 = GamePlayer.objects.create(acount='wyh99999',agent=agent1,block_id=1,)
        player2 = GamePlayer.objects.create(acount='player2',agent=agent1,block_id=1,par=player1)
        
        dc = {"row":{"amount":578,
                    "_director_name":"recharge_mb.form",
                    "game":1,
                    "block":1,
                    "character":10000000017416,
                    "account":"wyh99999",
                    "recharge_amount":1,
                    "_character_label":"啊啊啊哈哈",
                    }
                 }
        
        # player1充值1块
        rt = cl.post('/dapi/d.save_row',data=json.dumps(dc),content_type="application/json")
        player1.refresh_from_db()
        self.assertTrue( player1.credit ==1 )  
        
        dc = {"row":{"amount":4999,
                    "_director_name":"recharge_mb.form",
                    "game":1,
                    "block":1,
                    "character":10000000017416,
                    "account":"player2",
                    "recharge_amount":1000,
                    "_character_label":"啊啊啊哈哈",
                    }
                      }
        #player2充值1000,player1得到30
        rt2 = cl.post('/dapi/d.save_row',data=json.dumps(dc),content_type="application/json")
        player1.refresh_from_db()
        self.assertTrue( player1.credit ==301 )   
        
        
        # 测试签到
        # ==============
        today =timezone.now()
        for i in range(64):
            today = today + timezone.timedelta(days=1)
            self.mock_now.return_value = today
            
            dc ={"row":{"_director_name":"everyday-sign","meta_org_dict":{},"game":1,"block":1,"account":"wyh99999"}}
            rt = cl.post('/dapi/d.save_row',data=json.dumps(dc),content_type="application/json")
            memo = EverdaySign.objects.order_by('-createtime').first().memo
            print(today,memo)
            rt.json()
            
        # 测试签到断档
        print('模拟签到断档')
        count =0
        ratio = 1
        for i in range(40):
            count += 1
            today = today + timezone.timedelta(days=1)
            if count % (ratio * 5)==2:
                today = today + timezone.timedelta(days=1)
                ratio += 3
            self.mock_now.return_value = today
            
            dc ={"row":{"_director_name":"everyday-sign","meta_org_dict":{},"game":1,"block":1,"account":"wyh99999"}}
            rt = cl.post('/dapi/d.save_row',data=json.dumps(dc),content_type="application/json")
            memo = EverdaySign.objects.order_by('-createtime').first().memo
            print(today,memo)
            rt.json()        
        
        