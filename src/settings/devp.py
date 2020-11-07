from .base import *

import pymysql

pymysql.install_as_MySQLdb()


DATABASES = {
     'default': {
        'NAME': 'game_agent',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'root123456789',
        'HOST': '127.0.0.1', 
        'PORT': '3306', 
        'OPTIONS': {'charset':'utf8mb4'},
      },

} 