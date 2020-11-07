from django.contrib import admin
from helpers.case.jb_admin.admin_user import UserPage,UserFields,Group
# Register your models here.

from . import admin_agentuser
from . import admin_recharge

Group.objects.get_or_create(name='代理人')
