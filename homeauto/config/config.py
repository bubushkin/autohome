'''
Created on Nov 26, 2018

@author: iaskarov
'''

import logging;

class Config(object):
    
    DB_HOST = None;
    DB_USER = None;
    DB_PASSWD = None;    
    DB_NAME = None;
    LOG_LEVEL = None;
    DEBUG = False;
    TESTING = False;
    ENV = None;
    EMAIL = '';
    EMAIL_PASSWD = '';
    SMTP_SERVER = 'imap.gmail.com';
    SMTP_PORT = 993;
    DEVICE_CONF = "/var/www/html/webapps/homeautobot/devices.json";

class DevelopmentConfig(Config):
    
    DB_HOST = "";
    DB_USER = "";
    DB_PASSWD = "";    
    DB_NAME = "";
    LOG_LEVEL = logging.DEBUG;
    DEBUG = True;
    TESTING = True;
    ENV = 'development'

class ProductionConfig(Config):
    
    DB_HOST = "";
    DB_USER = "";
    DB_PASSWD = "";    
    DB_NAME = "";
    LOG_LEVEL = logging.INFO;
    DEBUG = False;
    TESTING = False;

config = {
    'production': ProductionConfig(),
    'development': DevelopmentConfig()
    }