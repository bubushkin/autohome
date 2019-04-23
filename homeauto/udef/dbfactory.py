'''
Created on Nov 26, 2018

@author: iaskarov
'''


from flask import current_app;
import sys;
from types import NoneType;
from flask import session;
import MySQLdb;
import traceback;

class DBFactory(object):
    
    _conn = None;

    def __init__(self, config):
            self.__config = config;
            self.__connect();
            
    def close(self):
        self._conn.close();
    
    def __connect(self):
        try:
            
            self._conn = MySQLdb.connect(self.__config["DB_HOST"], 
                                         self.__config["DB_USER"],
                                         self.__config["DB_PASSWD"],
                                         self.__config["DB_NAME"]); 
            check = self._conn.ping(False);
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
            sys.exit(0x1);
    
    def get_device_by_name(self, device_name):

        cursor = None;
        device = None;
        try:
            cursor = self._conn.cursor(MySQLdb.cursors.DictCursor);
            cursor.execute("SELECT device_id, device_name, device_io, device_couple, device_status, registration_timestamp FROM device WHERE device_name=%s", [device_name]);
            rset = cursor.fetchone();
            if not (isinstance(rset, NoneType)):
                device = rset;
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();
        return device;

    def get_action_by_name(self, status_name):

        cursor = None;
        device = None;
        try:
            cursor = self._conn.cursor(MySQLdb.cursors.DictCursor);
            cursor.execute("SELECT status_id, status_name FROM device_status WHERE status_name=%s", [status_name]);
            rset = cursor.fetchone();
            if not (isinstance(rset, NoneType)):
                device = rset;
        except MySQLdb.DatabaseError as ex:
            traceback.print_exc();
        finally:
            cursor.close();
        return device;
