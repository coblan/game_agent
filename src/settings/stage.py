from .base import *

import pymysql

pymysql.install_as_MySQLdb()

DATABASES = {
     'default': {
        'NAME': 'game_agent',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'zhou',
        'PASSWORD': 'zhou570508',
        'HOST': '172.18.215.159', 
        'PORT': '3306', 
        'OPTIONS': {'charset':'utf8mb4'},

      },
     'game_sqlserver': {
         'NAME': 'bnsm_gamedb_trunk_individual',#'Sports',
         'ENGINE': 'sql_server.pyodbc',
          'HOST':'120.79.245.189,10824', 
          'USER':  'sa',
         'PASSWORD': 'libi@123', 
         'OPTIONS': {
              'driver': 'ODBC Driver 17 for SQL Server',
             #'autocommit': True,
             #'host_is_server': True,
             #'unicode_results': True,
             #'driver': 'FreeTDS',
             #'extra_params': 'tds_version=8.0',
             
               },
                
        } ,      
} 

ALLOWED_HOSTS=['*']

SELF_DOMAIN = 'http://gameagent.enjoyst.com'