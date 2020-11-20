from helpers.director.shortcut import model_to_name, model_full_permit, add_permits, model_read_permit
from .models import GamePlayer,Recharge
import json

permits = [
    ('GamePlayer', model_read_permit(GamePlayer), model_to_name(GamePlayer), 'model' ),
    ('GamePlayer_desp',json.dumps({'write':['desp']}) , model_to_name(GamePlayer), 'model' ),
    #('GamePlayer.edit', model_full_permit(GamePlayer), model_to_name(GamePlayer) , 'model'), 
    ('Recharge', model_read_permit(Recharge), model_to_name(Recharge), 'model' ),
]
add_permits(permits)