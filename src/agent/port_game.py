import requests

def game_recharge(id_N,qty,pwd_P=None):
    '''id_N:玩家id
    qty: 数量
    pwd_P:物品标示
    '''
    print('发送物品数量:%s;接受玩家:%s'%(qty,id_N) )