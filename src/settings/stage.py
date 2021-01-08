from .base import *

import pymysql

pymysql.install_as_MySQLdb()

#DATABASES = {
     #'default': {
        #'NAME': 'game_agent',
        #'ENGINE': 'django.db.backends.mysql',
        #'USER': 'zhou',
        #'PASSWORD': 'zhou570508',
        #'HOST': '172.18.215.159', 
        #'PORT': '3306', 
        #'OPTIONS': {'charset':'utf8mb4'},

      #},
     #'game_sqlserver': {
         #'NAME': 'bnsm_gamedb_trunk_individual',#'Sports',
         #'ENGINE': 'sql_server.pyodbc',
          #'HOST':'120.79.245.189,10824', 
          #'USER':  'sa',
         #'PASSWORD': 'libi@123', 
         #'OPTIONS': {
              #'driver': 'ODBC Driver 17 for SQL Server',
             ##'autocommit': True,
             ##'host_is_server': True,
             ##'unicode_results': True,
             ##'driver': 'FreeTDS',
             ##'extra_params': 'tds_version=8.0',
             
               #},
                
        #} ,      
#} 

DATABASES = {
     'default': {
        'NAME': 'game_agent_stage',
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
     'game_sqlserver2': {
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

SELF_DOMAIN = 'http://test.bkpiyaso.cn'

DEV_NAME = '代理人[测试]'

GAMES = [
    {'label':'剑灵革命',
     'id':1,
     'blocks':[
         {'id':1,'db':'game_sqlserver','label':'第一区','charge_api':'http://101.132.98.232:7777/s1/item_result.php'},
         {'id':2,'db':'game_sqlserver2','label':'第二区','charge_api':'http://101.132.98.232:7777/s1/item_result.php'},
     ]}
]