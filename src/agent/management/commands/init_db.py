from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
import logging
general_log = logging.getLogger('general_log')
from helpers.case.jb_admin.admin_user import UserPage,UserFields,Group,PermitModel

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        group , _ = Group.objects.get_or_create( id =1 )
        group.name = '代理人'
        group.save()
        md , _ = PermitModel.objects.get_or_create(group=group)
        permits =['GamePlayer','Recharge','-agent_constraint']
        md.names= ';'.join(permits)
        md.save()


