from helpers.director.shortcut import director

def get_permit_show():
    return [
         {'label':'玩家管理','children':[
               {'label': '查看', 'value': 'GamePlayer',}, 
             ]},
    ]

director.update({
    'permit.options':get_permit_show,
})