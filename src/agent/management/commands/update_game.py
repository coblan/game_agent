from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
import logging
general_log = logging.getLogger('general_log')
from agent.models import Game,GameBlock,GamePlayer
from django.conf import settings

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        for game in settings.GAMES:
            g , _ = Game.objects.get_or_create( id =game.get('id') )
            g.name = game.get('label')
            g.save()
            for block in game.get('blocks'):
                b,_ = GameBlock.objects.get_or_create(id=block.get('id'),game=g )
                b.name = block.get('label')
                b.db = block.get('db')
                b.charge_api = block.get('charge_api')
                b.save()
        
        for palyer in GamePlayer.objects.all():
            palyer.save()

