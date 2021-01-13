from .base import *

import pymysql

pymysql.install_as_MySQLdb()


DATABASES = {
     #'default': {
        #'NAME': 'game_agent',
        #'ENGINE': 'django.db.backends.mysql',
        #'USER': 'root',
        #'PASSWORD': 'root123456789',
        #'HOST': '127.0.0.1', 
        #'PORT': '3306', 
        #'OPTIONS': {'charset':'utf8mb4'},
      #},
     'default': {
        'NAME': 'game_agent',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '47.113.186.102', 
        'PORT': '10822', 
        'OPTIONS': {'charset':'utf8mb4'},
      },     
     
     
     
     
     'game_sqlserver': {
         'NAME': 'bnsm_gamedb_trunk_individual',#'Sports',
         'ENGINE': 'sql_server.pyodbc',
          'HOST':'120.79.245.189,10824',
          'USER':  'sa',
         'PASSWORD': 'libi@123', 
         'OPTIONS': {
              
               },
                
        } , 
     'game_sqlserver2': {
         'NAME': 'bnsm_gamedb_trunk_individual',#'Sports',
         'ENGINE': 'sql_server.pyodbc',
          'HOST':'120.79.245.189,10824',
          'USER':  'sa',
         'PASSWORD': 'libi@123', 
         'OPTIONS': {
              
               },
                
        } ,      
} 

SELF_DOMAIN = 'http://localhost:8300'

GAME_PROXY = {
     'http':'socks5://47.113.186.102:10888',
      'https':'socks5://47.113.186.102:10888',
}

DEV_NAME = 'Test'

GAMES = [
    {'label':'剑灵革命',
     'id':1,
     'blocks':[
         {'id':1,'db':'game_sqlserver','label':'第一区','charge_api':'http://101.132.98.232:7777/s1/item_result.php'},
         {'id':2,'db':'game_sqlserver2','label':'第二区','charge_api':'http://101.132.98.232:7777/s1/item_result.php'},
     ]}
]