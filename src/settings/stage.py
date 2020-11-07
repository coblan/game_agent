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
} 

ALLOWED_HOSTS=['*']
