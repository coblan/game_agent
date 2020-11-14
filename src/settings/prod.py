from .base import *

import pymysql

pymysql.install_as_MySQLdb()

DATABASES = {
     'default': {
        'NAME': 'game_agent',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'root898767',
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
} 

ALLOWED_HOSTS=['*']

SELF_DOMAIN = 'http://gameagent.enjoyst.com'