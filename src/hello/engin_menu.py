
from helpers.director.shortcut import page_dc
from helpers.director.engine import BaseEngine, page, fa, can_list, can_touch
from django.contrib.auth.models import User, Group
from helpers.func.collection.container import evalue_container
from helpers.maintenance.update_static_timestamp import js_stamp
from django.utils.translation import ugettext as _
from django.conf import settings
from helpers.director.access.permit import has_permit

from django.utils import timezone

class PcMenu(BaseEngine):
    url_name = 'game_agent_admin'
    title = '代理人系统'
    brand = '代理人系统'
    mini_brand = '代理'
    need_staff=True
    access_from_internet=True
    
    @property
    def menu(self):
        crt_user = self.request.user
        menu = [
            {'label':'首页','url':page('enginhome'),'icon': fa('fa-home')},
          
            {'label':'充值记录','url':page('recharge'),'icon': fa('fa-cny'), 'visible': True},
            {'label': '代理人管理', 'url': page('agentuser'), 'icon': fa('fa-user-circle-o'), 'visible': True},
            
            #{'label': '域名列表', 'url': page('domain'), 'icon': fa('fa-clock-o'), 'visible': True},

            #{'label':'系统管理','url':page('cfg_admin'),'icon':fa('fa-clock-o'),'visible':crt_user.username=='admin'},
            {'label': '系统管理', 'icon': fa('fa-gear'), 'visible': True,
             'submenu': [
                 {'label': '账号管理', 'url': page('jb_user'), 'visible': can_touch(User, crt_user)},
                 {'label': '权限分组', 'url': page('jb_group'), 'visible': can_touch(Group, crt_user)},
                
                 #{'label':'设置管理','url':page('mycfg')},
                 #{'label':'运行日志','url':page('general_log')},
                 #{'label':'操作日志','url':page('backendoperation_log')}
             ]},
        ]

        return menu
    
    def custome_ctx(self, ctx):
        ctx['extra_js'] = ctx.get('extra_js',[])
        ctx['extra_js'].append('data_chart')
        ctx['menu_search'] = False
        return ctx

PcMenu.add_pages(page_dc)


