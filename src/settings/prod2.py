from .base import *

import pymysql

pymysql.install_as_MySQLdb()

DATABASES = {
     'default': {
        'NAME': 'game_agent2',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1', 
        'PORT': '3306', 
        'OPTIONS': {'charset':'utf8mb4'},

      },
     'game_sqlserver': {
         'NAME': 'bnsm_gamedb_trunk_individual',#'Sports',
         'ENGINE': 'sql_server.pyodbc',
          'HOST':'106.14.15.45,1433', 
          'USER':  'sa',
         'PASSWORD': 'libi@123', 
         'OPTIONS': {
              'driver': 'ODBC Driver 17 for SQL Server',

               },
                
        } ,   
     'game_sqlserver': {
         'NAME': 'bnsm_gamedb_trunk_individual',#'Sports',
         'ENGINE': 'sql_server.pyodbc',
          'HOST':'106.14.15.45,1433', 
          'USER':  'sa',
         'PASSWORD': 'libi@123', 
         'OPTIONS': {
              'driver': 'ODBC Driver 17 for SQL Server',

               },
                
        } ,        
} 

ALLOWED_HOSTS=['*']
DEBUG =False
SELF_DOMAIN = 'http://47.113.186.102'
GAME_PROXY ={}


BRAND_NAME='金牌代理'
THEME='skin-green-light'


GAMES = [
    {'label':'剑灵革命',
     'id':1,
     'blocks':[
         {'id':1,'db':'game_sqlserver','label':'第一区','charge_api':'http://101.132.98.232:7777/s1/item_result.php'},
         {'id':2,'db':'game_sqlserver2','label':'第二区','charge_api':'http://101.132.98.232:7777/s1/item_result.php'},
     ]}
]