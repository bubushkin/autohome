'''
Created on Nov 26, 2018

@author: iaskarov
'''

class FatalException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)    

class errno(object):
    
    HTTP_SUCCESS = 200;
    HTTP_SRV_FAILURE = 500;
    HTTP_CLT_FAILURE = 400;
    
    DB_CONN_ERR = "Database connection closed.";
    
    HTTP_NOT_FOUND = 404;
    
    EXIT_FAILURE = 0x1;
    EXIT_SUCCESS = 0x0;
    
    CONFIG_TYPE = { 'development': 0x1,
                    'production': 0x2,
                   }