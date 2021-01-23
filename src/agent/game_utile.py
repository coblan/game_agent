from .game_models import TbCharacter
from .models import GameBlock

def check_account_exist(account,block,game=1):
    block_inst = GameBlock.objects.get(pk= block)
    return TbCharacter.objects.using(block_inst.db).filter(account_id=account).exists()