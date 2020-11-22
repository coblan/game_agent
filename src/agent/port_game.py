import requests
from django.conf import settings
import re
import logging

general_log = logging.getLogger('general_log')

def game_recharge(id_N,qty,pwd_P=None):
    '''id_N:玩家id
    qty: 数量
    pwd_P:物品标示
    '''
    rt = re.search('^10+(\d+)',str(id_N) )
    id_N_id = rt.group(1)
    url = 'http://101.132.98.232:7777/s1/item_result.php'
    data = {
        "id_N": id_N_id,
        "pwd_P": pwd_P,
        "qty": qty,
        "Submit": "确认发货"        
    }
    rt = requests.post(url,data=data,proxies= getattr(settings,'GAME_PROXY',{}) )
    if rt.status_code == 200:
        general_log.debug('发送物品:%s;发送物品数量:%s;接受玩家:%s'%(pwd_P,qty,id_N) )
    else:
        general_log.error('发送物品服务器报错%s'% rt.text )
        raise UserWarning('发送物品服务器报错,请联系管理员')

def sss():
    print('ss')