"""
settings.py

Configuration for Flask app

Important: Place your keys in the secret_keys.py module, 
           which should be kept out of version control.

"""
from secret_keys import CSRF_SECRET_KEY, SESSION_KEY


class Config(object):
    # Set secret keys for CSRF protection
    SECRET_KEY = CSRF_SECRET_KEY
    CSRF_SESSION_KEY = SESSION_KEY
    # Flask-Cache settings
    CACHE_TYPE = 'gaememcached'
    LANGUAGES = {'en': ('English'), 'fr': ('French'), 'zh': ('Chinese')}
    ADMIN = ['lutianming1005@gmail.com']
    CONTACT = ['ZHU Qi <realzhq@gmail.com>',
               'ZHANG Nan <nan.zhann@gmail.com>',
               'DENG Ken <dengken524@live.cn>',
               'ZHU Tong <zhutong0114@gmail.com>',
               'Antoine ORY-LAMBALLE <antoine.orylamballe@yahoo.fr>',
               'Tianming LU <lutianming1005@gmail.com>']
    CC = ['ZHU Qi <realzhq@gmail.com>',
          'ZHANG Nan <nan.zhann@gmail.com>',
          'DENG Ken <dengken524@live.cn>',
          'ZHU Tong <zhutong0114@gmail.com>',
          'Antoine ORY-LAMBALLE <antoine.orylamballe@yahoo.fr>',
          'Tianming LU <lutianming1005@gmail.com>']
    SENDER = 'AFCP <admin@afcp-paristech.com>'
   
class Development(Config):
    DEBUG = True
    # Flask-DebugToolbar settings
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CSRF_ENABLED = True


class Testing(Config):
    TESTING = True
    DEBUG = True
    CSRF_ENABLED = True


class Production(Config):
    DEBUG = False
    CSRF_ENABLED = True
