# -*- coding: UTF-8 -*- 
VERSION = '1.0'


DEBUG = True


HOST = '10.3.0.92'


PORT = 8081


SECRET_KEY = 'PowerTeamSecret'

PAGESIZE = 10

import os
UPLOADDIR = 'static/upload/'
UPLOADPATH = os.path.join(os.path.dirname(__file__),UPLOADDIR)


DEFAULT_PASSWORD = '123'

ENABLE_MAIL_NOTICE = False

SMTP_HOST = 'smtp.qq.com'

SMTP_USER = 'test@qq.com'

SMTP_PASS = 'test'

DB = 'sqlite:///PowerTeam.db'

#'mysql://username:password@host:port/database'

#BAE
#from bae.core import const
#DB = 'mysql://'+const.MYSQL_USER+':'+const.MYSQL_PASS+'@'+const.MYSQL_HOST+':'+const.MYSQL_PORT+'/database' 

#SAE
#import sae.const
#DB = 'mysql://'+sae.const.MYSQL_USER+':'+sae.const.MYSQL_PASS+'@'+sae.const.MYSQL_HOST+':'+sae.const.MYSQL_PORT+'/'+sae.const.MYSQL_DB