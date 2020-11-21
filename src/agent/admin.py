from django.contrib import admin
from helpers.case.jb_admin.admin_user import UserPage,UserFields,Group
# Register your models here.

from . import admin_agentuser
from . import admin_recharge
from . import admin_agent_recharge
from . import admin_store
from . import admin_player

from . import admin_game
#Group.objects.get_or_create(name='代理人')

from . mobilepage import home
from . mobilepage import palyer_credit
from . mobilepage import player_store
from . import admin_home

from . import permit